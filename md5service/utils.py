import functools
from http import HTTPStatus
from json import JSONDecodeError

import pydantic
from aiohttp import web


def validate_request_dto(dto_cls):
    def wrapper(handler):
        @functools.wraps(handler)
        async def inner(request: web.Request):
            try:
                data = await request.json()
                data = dto_cls(**data)
            except JSONDecodeError:
                return web.json_response(
                    status=HTTPStatus.BAD_REQUEST,
                    data={"status": "error", "msg": "bad json"},
                )
            except pydantic.ValidationError as err:
                return web.json_response(status=HTTPStatus.BAD_REQUEST, data=err.json())

            return handler(request, data)

        return inner

    return wrapper
