from email.mime.text import MIMEText

from src.mail.connection import SmtpServer


class Mailer:
    def __init__(self, smtp_server: SmtpServer) -> None:
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
