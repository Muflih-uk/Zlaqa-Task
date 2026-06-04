import asyncio
from dataclasses import dataclass
from typing import Any

import aiohttp


@dataclass
class Result:
    url: str
    data: Any = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


async def _fetch_one(
    session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore
) -> Result:
    """Fetch a single URL, isolated so one failure won't abort others."""
    async with sem:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return Result(url=url, data=data)

        except Exception as exc:
            return Result(url=url, error=str(exc))


async def fetch_parallel(
    urls: list[str],
    max_concurrency: int = 5,
) -> list[Result]:
    """Fan out HTTP GET requests, cap inflight with a semaphore."""
    sem = asyncio.Semaphore(max_concurrency)
    async with aiohttp.ClientSession() as session:
        tasks = [_fetch_one(session, url, sem) for url in urls]
        results: list[Result] = await asyncio.gather(*tasks)
    return results


async def main():
    endpoints = [
        f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 11)
    ]
    results = await fetch_parallel(endpoints, max_concurrency=5)

    ok = [r for r in results if r.ok]
    err = [r for r in results if not r.ok]
    print(f"✓ {len(ok)} succeeded  ✗ {len(err)} failed")
    for r in err:
        print(f"  FAILED {r.url} — {r.error}")


asyncio.run(main())
