import asyncio
from dataclasses import dataclass, field

import httpx
from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import TimeoutTypes


@dataclass
class HTTPXClient(httpx.AsyncClient):
    timeout: TimeoutTypes = field(default=DEFAULT_TIMEOUT_CONFIG)

    def __post_init__(self):
        self.auth_params = {"app_id": self.app_id, "app_secret": self.app_secret}
        self.base_url = "https://qvapay.com/api/v1"
        self.http_client = AsyncClient(
            base_url=self.base_url,
            params=self.auth_params,
            timeout=self.timeout,
        )

    def request(self, method, url, *args, **kwargs):
        if self.is_async:
            return super().request(method, url, *args, **kwargs)
        else:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(super().request(method, url, *args, **kwargs))


# async def async_example():
#     async with CivoClient() as client:
#         response = await client.get("https://jsonplaceholder.typicode.com/posts/1")
#         print(response.text)


# def sync_example():
#     with CivoClient() as client:
#         response = client.get("https://jsonplaceholder.typicode.com/posts/1")
#         print(response.text)
