import httpx
from typing import Optional

class HttpFetcher:
    def __init__(self, timeout: float = 10.0):
        self.client = httpx.AsyncClient(timeout=timeout)

    async def fetch(self, url: str) -> tuple[int, str | None]:
        try:
            response = await self.client.get(url, follow_redirects=True)
            return response.status_code, response.text
        except Exception:
            return 0, None