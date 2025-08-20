import httpx
from src.utils.exceptions import AppException, HttpStatus


async def default_client(method: str, url: str, **kwargs) -> httpx.Response:
    """
    Create a default HTTP client for making requests.
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.request(method, url, **kwargs)
        return response
    

class Fetch:
    """
    A class to handle fetching data from a given URL.
    """

    def __init__(self, url: str, client: httpx.AsyncClient | None = None):
        """
        Initialize the Fetch class.
        """
        self.url = url
        self.client = client or default_client

    async def get(self, **kwargs) -> httpx.Response:
        """
        GET data from the URL.
        """
        return await self._handle_request("GET", **kwargs)

    async def post(self, **kwargs) -> httpx.Response:
        """
        POST data to the URL.
        """
        return await self._handle_request("POST", **kwargs)

    async def put(self, **kwargs) -> httpx.Response:
        """
        PUT data to the URL.
        """
        return await self._handle_request("PUT", **kwargs)

    async def _handle_request(self, method: str, **kwargs):
        """
        A centralized error handler for Fetch (get, post, etc.).
        """
        response = await self.client(method, self.url, **kwargs)
        if response.status_code == 400:
            raise AppException(HttpStatus.BAD_REQUEST, f"Bad request to {self.url}")
        elif response.status_code == 404:
            raise AppException(
                HttpStatus.NOT_FOUND, f"Resource at {self.url} not found"
            )
        elif response.status_code == 500:
            raise AppException(
                HttpStatus.INTERNAL_SERVER_ERROR, "Internal server error"
            )
        return response
