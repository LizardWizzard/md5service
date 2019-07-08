from pathlib import Path

import pytest
from aiohttp import web
from md5service import dto, mail
from md5service.app import make_app


@pytest.fixture
def client(loop, aiohttp_client):
    app = make_app()
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def sample_file_server(loop, aiohttp_server):
    sample_file_path = Path(__file__).absolute().parent / "md5testfile.txt"
    with open(sample_file_path, 'rb') as f:
        content = f.read()

    async def handler(req):
        return web.Response(body=content)

    app = web.Application()
    app.router.add_get("/file.txt", handler)

    return loop.run_until_complete(aiohttp_server(app))


@pytest.fixture
def sample_payload(sample_file_server):
    data = dto.SubmitRequest(
        url=f"http://{sample_file_server.host}:{sample_file_server.port}/file.txt",
        email=None,
    )
    return data


@pytest.fixture
def no_mail(mocker):
    async def empty(*args, **kwargs):
        pass

    # patch exclude performing such weird request and fill test logs with errors
    mocker.patch.object(mail, 'send_message', side_effect=empty)
