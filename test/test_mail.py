import unittest
from datetime import datetime
from telnetlib import SEND_URL

from rumad_monitor.src import config
from rumad_monitor.src.mail.connection import SmtpServer, SmtpTestServer
from rumad_monitor.src.mail.mailer import Mailer

SENDER_EMAIL = "send@sender.com"
TO_EMAIL = "receive@receiver.com"

TEST_SERVER = "localhost"
TEST_PORT = 1025


class MailerTest(unittest.TestCase):
    def test_connect(self):
        smtp_server = SmtpTestServer(SENDER_EMAIL, None, TEST_SERVER, TEST_PORT)
        mailer = Mailer(smtp_server)

        self.assertEqual(mailer.smtp, smtp_server)

    def test_send_mail(self):
        smtp_server = SmtpTestServer(SENDER_EMAIL, None, TEST_SERVER, TEST_PORT)
        mailer = Mailer(smtp_server)

        message = "Hi there, this is a Test."
        mailer.send_mail(TO_EMAIL, SENDER_EMAIL, message, "Test Email")

        recv = smtp_server.message_queue.get()

        self.assertEqual(SENDER_EMAIL, recv.get("from"))
        self.assertEqual(TO_EMAIL, recv.get("to"))

    @unittest.skipIf(
        config.INTEGRATION_TESTS.lower() == "false", "Integration tests disabled"
    )
    def test_integration(self):
        smtp_server = SmtpServer(
            sender_mail=config.FROM_EMAIL_ADDR,
            password=config.FROM_EMAIL_PASSWORD,
            smtp_server=config.SMTP_SERVER,
            port=config.SMTP_PORT,
        )

        mailer = Mailer(smtp_server)

        timestamp = datetime.now().isoformat()
        message = f"This is a message for the integration testing of RUMAD-Monitor.\n\nTimestamp: {timestamp}"

        mailer.send_mail(
            config.TO_EMAIL_ADDR.split(","),
            config.FROM_EMAIL_ADDR,
            message,
            "Integration test for RUMAD Monitor.",
        )

        smtp_server.quit()


if __name__ == "__main__":
    unittest.main()
