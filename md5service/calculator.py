import hashlib
import logging

import aiohttp
from aioredis import Redis
from md5service import dto

logger = logging.getLogger(__name__)


async def calc_by_url(url):
    async with aiohttp.ClientSession() as session:
        result = hashlib.md5()
        async with session.get(url) as resp:
            async for chunk in resp.content.iter_chunks():
                result.update(chunk)

        return result.hexdigest()


async def calc_task(task_uuid: str, task_state: dto.TaskState, redis: Redis):
    try:
        result = await calc_by_url(task_state.url)
    except Exception as e:
        logging.exception("Exception occurred during md5 calculation: %s", e)
        task_state.err = str(e)
        task_state.status = dto.TaskStatus.FAILED
    else:
        task_state.md5 = result
        task_state.status = dto.TaskStatus.DONE

    try:
        await redis.set(task_uuid, task_state.json())
    except Exception as e:
        logger.error("Failed to save task state: %s", e)

    # TODO email notification
