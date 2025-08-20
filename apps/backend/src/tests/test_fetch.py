import asyncio
import httpx
import pytest

from src.utils.fetch import Fetch, AppException, HttpStatus
from pytest_httpx import HTTPXMock


async def fetch_client(method: str, url: str, **kwargs) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        return await client.request(method, url, **kwargs)


@pytest.mark.asyncio
async def test_fetch_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.com",
        method="GET",
        status_code=200,
        json=[{"key": "value"}],
        headers={"Content-Type": "application/json"},
    )

    result = await Fetch("https://test.com", client=fetch_client).get()

    assert result.status_code == 200
    assert result.json() == [{"key": "value"}]
    assert result.headers["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_fetch_failure(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.com",
        method="GET",
        status_code=404,
        content=b"Not Found",
    )

    with pytest.raises(AppException) as exc_info:
        await Fetch("https://test.com", client=fetch_client).get()

        assert exc_info.value.status_code == HttpStatus.NOT_FOUND
        assert str(exc_info.value) == "Resource at https://test.com not found"


@pytest.mark.asyncio
def test_fetch_post(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.com",
        method="POST",
        status_code=201,
        json={"message": "Created"},
        headers={"Content-Type": "application/json"},
    )

    async def post_data():
        return await Fetch("https://test.com", client=fetch_client).post(
            json={"key": "value"}
        )

    result = asyncio.run(post_data())

    assert result.status_code == 201
    assert result.json() == {"message": "Created"}
    assert result.headers["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_fetch_post_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.com",
        method="POST",
        status_code=400,
        content=b"Invalid Request",
    )

    with pytest.raises(AppException) as exc_info:
        await Fetch("https://test.com", client=fetch_client).post(json={"key": "value"})

        assert exc_info.value.status_code == HttpStatus.BAD_REQUEST
        assert str(exc_info.value) == "Invalid request"


# write test for put method
@pytest.mark.asyncio
def test_fetch_put(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.com",
        method="PUT",
        status_code=200,
        json={"message": "Updated"},
        headers={"Content-Type": "application/json"},
    )

    async def put_data():
        return await Fetch("https://test.com", client=fetch_client).put(
            json={"key": "new_value"}
        )

    result = asyncio.run(put_data())

    assert result.status_code == 200
    assert result.json() == {"message": "Updated"}
    assert result.headers["Content-Type"] == "application/json"


# write test for error put method

@pytest.mark.asyncio
async def test_fetch_put_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.com",
        method="PUT",
        status_code=500,
        content=b"Internal Server Error",
    )

    with pytest.raises(AppException) as exc_info:
        await Fetch("https://test.com", client=fetch_client).put(json={"key": "value"})

        assert exc_info.value.status_code == HttpStatus.INTERNAL_SERVER_ERROR
        assert str(exc_info.value) == "Internal server error"
