import json
import logging
from asyncio import InvalidStateError
from collections import defaultdict
from datetime import datetime
from io import StringIO
from typing import List, Optional, Tuple, Union

from rumad_monitor.src import config
from rumad_monitor.src.controllers.rumad import RumadMonitor
from rumad_monitor.src.controllers.rumad.semesters import Semesters
from rumad_monitor.src.mail.connection import SmtpServer
from rumad_monitor.src.mail.mailer import Mailer
from rumad_monitor.src.models.section import Section
from rumad_monitor.src.vt100 import Terminal


class Courses:
    def __init__(
        self, courses_to_monitor: List[str], professors: List[Optional[str]]
    ) -> None:
        if len(courses_to_monitor) != len(professors):
            raise InvalidStateError(
                "Every course must have a matching Optional professor."
            )

        self.courses = defaultdict(list)

        for idx, course in enumerate(courses_to_monitor):
            self.add(course, professors[idx])

    def add(self, course_code, professors: Optional[Union[str, List[str]]] = None):
        if isinstance(professors, str):
            self.courses[course_code].append(professors)
        elif isinstance(professors, list):
            self.courses[course_code].extend(professors)
        else:
            self.courses[course_code]

    def get_courses(self) -> List[str]:
        return self.courses.keys()

    def get_professors(self, course_code) -> Optional[List[str]]:
        if course_code not in self.courses:
            return None
        return self.courses[course_code]

    def get_pairs(self) -> Tuple[str, List[str]]:
        return self.courses.items()


class Notification:
    def __init__(self, header) -> None:
        self.courses = []
        self.buffer = StringIO()
        self.buffer.write(header)

    def add_course(self, course: str, section: Section):
        self.courses.append((course, section))
        self.buffer.write(
            f"""Course: {course} (Section:"{section.code}") has a current availability of {section.remaining()} spaces.\n
Section details:\n{section.pretty()}\n"""
        )

    def dump(self) -> str:
        return self.buffer.getvalue()


courses_to_monitor = Courses(
    ["Inel4207", "Mate4031", "Icom4035"],
    [["Manuel Toledo"], ["Freddie Santiago"], ["Manuel Rodriguez"]],
)


def format(msg, **kwargs) -> str:
    return json.dumps({"time": datetime.now().isoformat(), "log": msg, **kwargs})


JOB_NAME = "Matricula-2021-Spring"

YEAR = 2021
SEMESTER = Semesters.Horario.SECOND


def start():
    logging.info(format(f"Start {JOB_NAME}"))

    monitor = RumadMonitor("horario", "", Terminal())

    preferred_notification = Notification("PREFERRED SECTIONS\n")
    regular_notification = Notification("ALL SECTIONS\n")

    for course, professors in courses_to_monitor.get_pairs():
        logging.debug(format("Start" + course))

        sections = monitor.get_sections(YEAR, 3, course)

        for section in sections:
            if section.remaining() > 0:
                if section.prof.lower() in professors:
                    preferred_notification.add_course(course, section)
                else:
                    regular_notification.add_course(course, section)

    print("HA", "-" * 10)
    print(preferred_notification.dump())

    print("HA", "-" * 10)
    print(regular_notification.dump())

    if (
        len(preferred_notification.courses) == 0
        and len(regular_notification.courses) == 0
    ):
        logging.info(format(f"End {JOB_NAME}"))
        return

    content = ""

    if len(preferred_notification.courses) > 0:
        content += preferred_notification.dump()

    if len(regular_notification.courses) > 0:
        content += "\n" + regular_notification.dump()

    smtp_server = SmtpServer(
        sender_mail=config.FROM_EMAIL_ADDR,
        password=config.FROM_EMAIL_PASSWORD,
        smtp_server=config.SMTP_SERVER,
        port=config.SMTP_PORT,
    )

    mailer = Mailer(smtp_server)

    mailer.send_mail(
        subject="RUMAD Monitor Available Section Notification",
        send_from=config.FROM_EMAIL_ADDR,
        send_to=config.TO_EMAIL_ADDR,
        text=content,
    )

    smtp_server.quit()


if __name__ == "__main__":
    start()
