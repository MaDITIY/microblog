from threading import Thread
from typing import Iterable

from flask import current_app
from flask_mail import Message

from app import mail


def send_email(
        subject: str,
        sender: str,
        recipients: list,
        text_body: str,
        html_body: str,
        attachments: Iterable = tuple(),
        send_async: bool = False,
) -> None:
    """Start a new thread to send email."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    for attachment in attachments:
        msg.attach(*attachment)
    if send_async:
        Thread(
            target=send_async_email,
            args=(current_app._get_current_object(), msg)
        ).start()
    else:
        mail.send(msg)


def send_async_email(app, msg):
    """Send email."""
    with app.app_context():
        mail.send(msg)
