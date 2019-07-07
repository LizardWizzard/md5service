import asyncio
from dataclasses import dataclass
from email.mime.text import MIMEText

import aiosmtplib
from md5service import dto


@dataclass
class SMTPConfig:
    host: str
    port: int


async def send_message(task_state: dto.TaskState, smtpconf: SMTPConfig):
    message = MIMEText("")
    message["From"] = "admin@md5service.local"
    message["To"] = task_state.email
    message["Subject"] = "Md5 calculation result"

    async with aiosmtplib.SMTP(
        hostname=smtpconf.host, port=smtpconf.port, loop=asyncio.get_event_loop()
    ) as smtp:
        await smtp.send_message(message)
        # TODO record error
