import queue
import smtplib
from typing import Sequence, Union


class SmtpServer(smtplib.SMTP):
    def __init__(self, sender_mail, password, smtp_server, port) -> None:
        super().__init__(smtp_server, port)
        # Create your SMTP session

        self.sender_mail = sender_mail

        self.ehlo()

        # Use TLS to add security
        try:
            self.starttls()
            self.ehlo()
        except:
            pass

        # User Authentication
        if password:
            self.login(sender_mail, password)

    def __del__(self):
        try:
            self.quit()
        except:
            pass


class SmtpTestServer(SmtpServer):
    def __init__(self, sender_mail, password, smtp_server, port) -> None:
        self.message_queue: queue.Queue = queue.Queue()

    def sendmail(
        self,
        from_addr: str,
        to_addrs: Union[str, Sequence[str]],
        msg: Union[bytes, str],
        mail_options: Sequence[str] = ...,
        rcpt_options: Sequence[str] = ...,
    ):
        self.message_queue.put({"message": msg, "to": to_addrs, "from": from_addr})

    def close(self) -> None:
        return

    def __del__(self):
        return
