import unittest

from rumad_monitor.src.mail import Mailer, SmtpTestServer
from rumad_monitor.src.models import MailBuilder
from src.models.notifications import Notification
from src.models.section import Section


def create_mbuilder():
    job_name = "test1"

    smtp_server = SmtpTestServer(
        sender_mail="sender1@test.com",
        password="test",
        smtp_server="test.tester.org",
        port=587,
    )

    mailer = Mailer(smtp_server)

    return MailBuilder(job_name=job_name, mailer=mailer), smtp_server


def create_notification(name: str, ccode: str):
    notification = Notification(name)

    section = Section(
        "070      LW     1:30- 3:20pm    4   ROBERT ACAR   30    19    11"
    )
    notification.add_course(ccode, section)

    return notification


class TestMailBuilder(unittest.TestCase):
    def test_mail_builder(self):
        m_builder, smtp_server = create_mbuilder()
        notif_1 = create_notification("notification 1", "test1")

        m_builder.add_notification(notif_1)

        m_builder.send_notification("sender@test.com", "receiver@test.org")

        self.assertEqual(
            smtp_server.message_queue.get()["message"],
            'Content-Type: text/plain; charset="us-ascii"\n'
            "MIME-Version: 1.0\n"
            "Content-Transfer-Encoding: 7bit\n"
            "Subject: RUMAD Monitor Available Section Notification\n"
            "From: sender@test.com\n"
            "\n"
            'Job Name: "TEST1"\n'
            "----------------------------------------\n"
            "\n"
            "\n"
            "NOTIFICATION 1:\n"
            "\n"
            'Course: TEST1 (Section:"070") has a current availability of 11 spaces.\n'
            "\n"
            "Section details:\n"
            "    - Code: 070\n"
            "    - Professor: ROBERT ACAR\n"
            "    - Time: LW 1:30-3:20PM\n"
            "    - Credits: 4\n"
            "    - Capacity: 30\n"
            "    - Used spaces: 19\n"
            "    - Remaining spaces: 11\n",
        )

    def test_mail_builder_multiple_notifications(self):
        m_builder, smtp_server = create_mbuilder()
        notif_1 = create_notification("notification 1", "test1")
        notif_2 = create_notification("notification 2", "test2")

        m_builder.add_notification(notif_1)
        m_builder.add_notification(notif_2)

        m_builder.send_notification("sender@test.com", "receiver@test.org")

        self.assertEqual(
            smtp_server.message_queue.get()["message"],
            'Content-Type: text/plain; charset="us-ascii"\n'
            "MIME-Version: 1.0\n"
            "Content-Transfer-Encoding: 7bit\n"
            "Subject: RUMAD Monitor Available Section Notification\n"
            "From: sender@test.com\n"
            "\n"
            'Job Name: "TEST1"\n'
            "----------------------------------------\n"
            "\n"
            "\n"
            "NOTIFICATION 1:\n"
            "\n"
            'Course: TEST1 (Section:"070") has a current availability of 11 spaces.\n'
            "\n"
            "Section details:\n"
            "    - Code: 070\n"
            "    - Professor: ROBERT ACAR\n"
            "    - Time: LW 1:30-3:20PM\n"
            "    - Credits: 4\n"
            "    - Capacity: 30\n"
            "    - Used spaces: 19\n"
            "    - Remaining spaces: 11\n"
            "\n"
            "NOTIFICATION 2:\n"
            "\n"
            'Course: TEST2 (Section:"070") has a current availability of 11 spaces.\n'
            "\n"
            "Section details:\n"
            "    - Code: 070\n"
            "    - Professor: ROBERT ACAR\n"
            "    - Time: LW 1:30-3:20PM\n"
            "    - Credits: 4\n"
            "    - Capacity: 30\n"
            "    - Used spaces: 19\n"
            "    - Remaining spaces: 11\n",
        )


if __name__ == "__main__":
    unittest.main()
