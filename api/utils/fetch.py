import httpx
from api.utils.exceptions import AppException, HttpStatus


class Fetch:
    """
    A class to handle fetching data from a given URL.
    """

    def __init__(self, url: str):
        self.url = url

    async def get(self, **kwargs) -> httpx.Response:
        """
        GET data from the URL.
        """

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(self.url, **kwargs)
            if response.status_code == 404:
                raise AppException(
                    HttpStatus.NOT_FOUND, f"Resource at {self.url} not found"
                )
            elif response.status_code == 500:
                raise AppException(
                    HttpStatus.INTERNAL_SERVER_ERROR, "Internal server error"
                )
            elif response.status_code == 200:
                return response
