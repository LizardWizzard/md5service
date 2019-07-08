from http import HTTPStatus

from md5service import dto, handlers


async def test_bad_json(client):
    resp = await client.post('/submit', data="not json")
    assert resp.status == HTTPStatus.BAD_REQUEST
    body = await resp.json()
    assert body == {"status": "error", "msg": "bad json"}


async def test_valid_payload(client, mocker):
    sample_payload = dto.SubmitRequest(url=f"http://some.local/file.txt", email=None)

    async def empty(*args, **kwargs):
        pass

    # patch exclude performing such weird request and fill test logs with errors
    mocker.patch.object(handlers.calculator, 'calc_task', side_effect=empty)

    mocker.patch.object(handlers.uuid, 'uuid4', return_value='constant_uuid')
    resp = await client.post('/submit', data=sample_payload.json())
    body = await resp.json()
    assert body == {"id": "constant_uuid"}
    assert resp.status == HTTPStatus.ACCEPTED
