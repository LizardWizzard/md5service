import asyncio
import logging
import os

import aioredis
from aiohttp import web
from dotenv import load_dotenv

from md5service.handlers import routes

logger = logging.getLogger('md5service')


async def init_redis(app: web.Application):
    redis = await aioredis.create_redis_pool(
        os.getenv("REDIS_URL"),  # TODO validate redis url
        minsize=5, maxsize=10,
        loop=asyncio.get_event_loop()
    )
    app['redis'] = redis
    logger.info('Redis connection initialized')


async def close_redis(app: web.Application):
    redis = app['redis']
    redis.close()
    await redis.wait_closed()
    logger.info('Redis connection closed')


def make_app() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    app.on_startup.append(init_redis)
    app.on_shutdown.append(close_redis)
    return app


if __name__ == '__main__':
    load_dotenv()
    web.run_app(
        port=os.environ.get("PORT"),  # TODO validate port
        app=make_app(),
        access_log_format='%a %t %Tf "%r" %s %b "%{Referer}i" "%{User-Agent}i"'
    )
