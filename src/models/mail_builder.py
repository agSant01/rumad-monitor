from typing import List

from rumad_monitor.src.mail.mailer import Mailer
from rumad_monitor.src.models.notifications import Notification


class MailBuilder:
    def __init__(self, job_name: str, mailer: Mailer) -> None:
        self.job_name: str = job_name.upper()
        self.mailer: Mailer = mailer
        self.notifications: List[Notification] = []

    def add_notification(self, notification: Notification):
        self.notifications.append(notification)

    def send_notification(self, send_from: str, send_to: str):
        content: List[str] = [f'Job Name: "{self.job_name}"', "-" * 40, "\n"]

        for notification in self.notifications:
            if len(notification.courses) == 0:
                continue

            content.append(notification.dump())

        if len(content) == 0:
            return

        message_to_send = "\n".join(content)

        self.mailer.send_mail(
            subject="RUMAD Monitor Available Section Notification",
            send_from=send_from,
            send_to=send_to,
            text=message_to_send,
        )
