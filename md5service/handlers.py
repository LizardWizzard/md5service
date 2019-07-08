import asyncio
import logging
import uuid
from http import HTTPStatus

from aiohttp import web
from aioredis import Redis
from md5service import calculator, dto
from md5service.utils import validate_request_dto

logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.post('/submit')
@validate_request_dto(dto.SubmitRequest)
async def submit(request: web.Request, data: dto.SubmitRequest) -> web.Response:
    task_uuid = str(uuid.uuid4())
    task_state = dto.TaskState.parse_obj(
        {'url': data.url, 'email': data.email, 'status': dto.TaskStatus.SCHEDULED}
    )

    redis: Redis = request.app['redis']
    try:
        await redis.set(task_uuid, task_state.json())
    except Exception as e:
        logger.error('Failed to save task state: %s', e)
        return web.json_response(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            data={'status': 'error', 'msg': 'Failed to save task state'},
        )

    loop = asyncio.get_event_loop()
    loop.create_task(
        calculator.calc_task(task_uuid, task_state, redis, request.app['smtpconf'])
    )

    return web.json_response({'id': task_uuid}, status=HTTPStatus.ACCEPTED)


@routes.post('/check')
@validate_request_dto(dto.CheckRequest)
async def check(request: web.Request, data: dto.CheckRequest):
    redis: Redis = request.app['redis']
    try:
        result = await redis.get(data.id)
    except Exception as e:
        logger.error('Failed to retrieve task state: %s', e)
        return web.json_response(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            data={'status': 'error', 'msg': 'Failed to retrieve task state'},
        )

    if not result:
        return web.json_response(
            status=HTTPStatus.NOT_FOUND, data={'status': 'not_found'}
        )

    # assumed that no one can change value we put to redis,
    # so values we can get are trusted and validation is redundant
    task_state = dto.TaskState.parse_raw(result)
    return web.json_response(task_state.dict(include={'md5', 'status', 'url', 'err'}))
