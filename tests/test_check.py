from http import HTTPStatus

from md5service import dto


async def test_404_response(client):
    payload = dto.CheckRequest(id="task does not exist").json()
    resp = await client.post('/check', data=payload)
    assert resp.status == HTTPStatus.NOT_FOUND
    body = await resp.json()
    assert body == {"status": "not_found"}
