import time
from typing import List, Set

import paramiko

import vt100
from models.section import Section, parse_sections

host = "rumad.uprm.edu"
port = 22
username = "horario"

term = vt100.Terminal(verbosity=False, height=25, width=80)


def send_cmd(
    cmd: str, channel: paramiko.Channel, wait=False, nbytes: int = 2048
) -> str:
    channel.send(cmd.encode())
    while not channel.recv_ready() and wait:
        time.sleep(1)
    data = channel.recv(nbytes)
    term.clear()
    term.parse(data.decode("Latin1"))
    return term.to_string()


def get_sections(channel, year, semester, course_code) -> Set[Section]:
    resp = send_cmd(str(year), channel, wait=True)
    resp = send_cmd(str(semester), channel, wait=True)

    resp = send_cmd(f"{course_code}\n", channel, wait=True)
    sections: List[str] = resp.splitlines()
    while "Curso Incorrecto" not in resp:
        try:
            resp = send_cmd("\n", channel, wait=True)
            sections += resp.splitlines()
        except Exception as e:
            print(e)
            break

    return parse_sections(sections)


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, "", timeout=1000)

    channel = ssh.invoke_shell()

    courses = get_sections(channel, 2022, 3, "inel4207")

    channel.close()
    ssh.close()

    print(courses)


if __name__ == "__main__":
    main()
