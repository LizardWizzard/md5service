import asyncio
import logging
import os

import aioredis
from aiohttp import web
from dotenv import load_dotenv
from md5service import mail
from md5service.handlers import routes

logger = logging.getLogger('md5service')

logging.basicConfig(level=logging.INFO)


async def init_redis(app: web.Application):
    redis = await aioredis.create_redis_pool(
        os.getenv("REDIS_URL"),  # TODO validate redis url
        minsize=5,  # TODO add to env config hardcoded values
        maxsize=10,
        loop=asyncio.get_event_loop(),
    )
    app['redis'] = redis
    logger.info('Redis connection initialized')


async def close_redis(app: web.Application):
    redis = app['redis']
    redis.close()
    await redis.wait_closed()
    logger.info('Redis connection closed')


def make_app() -> web.Application:
    load_dotenv()
    smtpconf = mail.SMTPConfig(host=os.getenv("SMTP_HOST"), port=os.getenv("SMTP_PORT"))
    app = web.Application()
    app['smtpconf'] = smtpconf
    app.add_routes(routes)
    app.on_startup.append(init_redis)
    app.on_shutdown.append(close_redis)
    return app


if __name__ == '__main__':
    web.run_app(port=os.environ.get("PORT"), app=make_app())  # TODO validate port
