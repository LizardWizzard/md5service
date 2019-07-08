import asyncio
from http import HTTPStatus

from md5service import dto, handlers


async def test_valid_md5(client, sample_payload, no_mail):
    resp = await client.post('/submit', data=sample_payload.json())
    body = await resp.json()
    task_uuid = body['id']
    assert resp.status == HTTPStatus.ACCEPTED

    # wait for background computation
    await asyncio.sleep(1)

    payload = dto.CheckRequest(id=task_uuid).json()
    resp = await client.post('/check', data=payload)
    assert resp.status == HTTPStatus.OK

    body = await resp.json()

    expected_payload = {
        'status': 'DONE',
        'url': sample_payload.url,
        'md5': 'b3158c20fa4dc0c4eba25fd8845d1d54',  # cat tests/md5testfile.txt | md5
        'err': '',
    }
    assert body == expected_payload


async def test_error(client, sample_payload, mocker, no_mail):
    async def error_task(*args, **kwargs):
        raise Exception("Unexpected error during computation")

    # patch exclude performing such weird request and fill test logs with errors
    mocker.patch.object(handlers.calculator, 'calc_by_url', side_effect=error_task)

    resp = await client.post('/submit', data=sample_payload.json())
    body = await resp.json()
    task_uuid = body['id']
    assert resp.status == HTTPStatus.ACCEPTED

    # wait for background computation
    await asyncio.sleep(1)

    payload = dto.CheckRequest(id=task_uuid).json()
    resp = await client.post('/check', data=payload)
    assert resp.status == HTTPStatus.OK

    body = await resp.json()

    expected_payload = {
        'status': 'FAILED',
        'url': sample_payload.url,
        'md5': '',
        'err': 'Unexpected error during computation',
    }
    assert body == expected_payload
