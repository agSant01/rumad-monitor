import json
import logging
from datetime import datetime

from src import config
from src.controllers.rumad import RumadMonitor
from src.controllers.rumad.semesters import Semesters
from src.mail.connection import SmtpServer
from src.mail.mailer import Mailer
from src.models.courses import Courses
from src.models.mail_builder import MailBuilder
from src.models.notifications import Notification
from src.vt100 import Terminal


def format(msg, **kwargs) -> str:
    return json.dumps({"time": datetime.now().isoformat(), "log": msg, **kwargs})


JOB_NAME = "Matricula-2021-Spring"

YEAR = 2021
SEMESTER = Semesters.Horario.SPRING_SEMESTER

courses_to_monitor = Courses(
    ["Inel4207", "Mate4031", "Icom4035"],
    [["Manuel Toledo"], ["Freddie Santiago"], ["Manuel Rodriguez"]],
)


def start_job():
    logging.info(format(f"Start_job {JOB_NAME}"))

    monitor = RumadMonitor("horario", "", Terminal())

    preferred_sections = Notification("PREFERRED SECTIONS")
    regular_sections = Notification("ALL SECTIONS")

    for course, professors in courses_to_monitor.get_pairs():
        logging.debug(format("Start_job" + course))

        sections = monitor.get_sections(YEAR, 3, course)

        for section in sections:
            if section.remaining() > 0:
                if section.prof.lower() in professors:
                    preferred_sections.add_course(course, section)
                else:
                    regular_sections.add_course(course, section)

    smtp_server = SmtpServer(
        sender_mail=config.FROM_EMAIL_ADDR,
        password=config.FROM_EMAIL_PASSWORD,
        smtp_server=config.SMTP_SERVER,
        port=config.SMTP_PORT,
    )

    mailer = Mailer(smtp_server)

    mail_builder = MailBuilder(job_name=JOB_NAME, mailer=mailer)

    mail_builder.add_notification(preferred_sections)
    mail_builder.add_notification(regular_sections)

    mail_builder.send_notification(
        send_from=config.FROM_EMAIL_ADDR,
        send_to=config.TO_EMAIL_ADDR,
    )

    smtp_server.quit()


if __name__ == "__main__":
    start_job()
