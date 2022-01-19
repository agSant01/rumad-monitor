import logging
import time
from typing import List, Set

import paramiko

from rumad_monitor.src import vt100
from rumad_monitor.src.controllers.sections import parse_sections
from rumad_monitor.src.models.section import Section

RUMAD_HOST = "rumad.uprm.edu"
RUMAD_PORT = "22"


class RumadMonitor:
    def __init__(
        self, username, password, virtual_term: vt100.Terminal, timeout=1000
    ) -> None:
        self.virtual_term = virtual_term
        self.username = username
        self.password = password
        self.timeout = timeout
        self.channel = None
        self.ssh = None
        self.refresh_connection()

    def refresh_connection(self):
        self.close()
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            RUMAD_HOST,
            RUMAD_PORT,
            username=self.username,
            password=self.password,
            timeout=self.timeout,
        )

        self.channel = self.ssh.invoke_shell()
        self.channel.setblocking(False)

    def get_sections(self, year, semester, course_code) -> Set[Section]:
        resp = self.__send_cmd(str(year))
        resp = self.__send_cmd(str(semester))
        resp = self.__send_cmd(f"{course_code}\n")
        resp = self.__send_cmd("\n")

        sections_: List[str] = resp.splitlines()

        while "Curso Incorrecto" not in resp and "FIN=Finalizar" not in resp:
            try:
                resp = self.__send_cmd("\n")
                # print(resp)
                sections_ += resp.splitlines()
            except Exception as e:
                print(e)
                break

        logging.debug("Finished sections")

        self.refresh_connection()

        return parse_sections(sections_)

    def close(self) -> None:
        self.virtual_term.clear()
        try:
            self.channel.close()
        except:
            pass
        try:
            self.ssh.close()
        except:
            pass

    def __parse_ansi(self, text: str) -> str:
        self.virtual_term.clear()
        self.virtual_term.parse(text)
        return self.virtual_term.to_string()

    def __send_cmd(self, cmd: str, nbytes: int = 2048 * 2) -> str:
        self.channel.send(cmd.encode())
        data = bytes()

        c = 0
        while True:
            r = bytes()
            if self.channel.recv_ready():
                r = self.channel.recv(nbytes)
                if len(r) <= 1:
                    break
            else:
                c += 1
                if c >= 4:
                    break
            data += r or bytes()
            time.sleep(2)

        return self.__parse_ansi(data.decode("Latin1"))

    def __del__(self) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"<RumadMonitor sshConnection:{self.ssh}>"
