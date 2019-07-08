import asyncio
from dataclasses import dataclass
from email.mime.text import MIMEText

import aiosmtplib
from md5service import dto


@dataclass
class SMTPConfig:
    host: str
    port: int


async def send_message(task_state: dto.TaskState, smtpconf: SMTPConfig, message_body):
    message = MIMEText(message_body)
    message["From"] = "admin@md5service.local"
    message["To"] = task_state.email
    message["Subject"] = "Md5 calculation result"

    async with aiosmtplib.SMTP(
        hostname=smtpconf.host, port=smtpconf.port, loop=asyncio.get_event_loop()
    ) as smtp:
        await smtp.send_message(message)
        # TODO record error


async def send_success(task_state: dto.TaskState, smtpconf: SMTPConfig):
    body = f"Your md5 was successfully calculated!\n\n\
    url: {task_state.url}, md5: {task_state.md5}"
    await send_message(task_state, smtpconf, body)


async def send_failure(task_state: dto.TaskState, smtpconf: SMTPConfig):
    body = f"Your md5 was not successfully calculated.\n\n\
    url: {task_state.url}, err: {task_state.err}"
    await send_message(task_state, smtpconf, body)
