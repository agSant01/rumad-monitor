import smtplib
from email.mime.text import MIMEText

# from connection import SmtpServer


class Mailer:
    def __init__(self, smtp_server) -> None:
        # Create your SMTP session
        self.smtp = smtp_server

    def send_mail(self, send_to, send_from, text, subject):
        message = MIMEText(_text=text)
        message["Subject"] = subject
        message["From"] = send_from

        # Sending the Email
        return self.smtp.sendmail(
            from_addr=send_from,
            to_addrs=send_to,
            msg=message.as_string(),
        )

    def close(self):
        self.__del__()

    def __del__(self):
        if hasattr(self, "smtp"):
            self.smtp.close()
