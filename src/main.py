import time
from typing import List, Set

import paramiko
from rumad_monitor.src import vt100

from .models.section import Section, parse_sections

host = "rumad.uprm.edu"
username = "horario"
port = 22

term = vt100.Terminal(verbosity=False, height=25, width=80)


def send_cmd(
    cmd: str, channel: paramiko.Channel, wait=False, nbytes: int = 4096
) -> str:
    channel.send(cmd.encode())
    data = bytes()

    c = 0
    while True:
        r = bytes()
        if channel.recv_ready():
            r = channel.recv(nbytes)
            if len(r) <= 1:
                break
        else:
            c += 1
            if c >= 4:
                break
        data += r or bytes()
        time.sleep(1)

    term.clear()
    term.parse(data.decode("Latin1"))
    return term.to_string()


def get_sections(channel, year, semester, course_code) -> Set[Section]:
    resp = send_cmd(str(year), channel, wait=True)

    resp = send_cmd(str(semester), channel, wait=True)
    resp = send_cmd(f"{course_code}\n", channel, wait=True)
    resp = send_cmd("\n", channel, wait=True)

    sections_: List[str] = resp.splitlines()
    # print(resp)

    while "Curso Incorrecto" not in resp and "FIN=Finalizar" not in resp:
        try:
            resp = send_cmd("\n", channel, wait=True)
            # print(resp)
            sections_ += resp.splitlines()
        except Exception as e:
            print(e)

    return parse_sections(sections_)


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, "", timeout=1000)

    channel = ssh.invoke_shell()
    channel.setblocking(False)

    courses = get_sections(channel, 2021, 3, "inel4207")

    channel.close()
    ssh.close()

    print(courses)


if __name__ == "__main__":
    main()
