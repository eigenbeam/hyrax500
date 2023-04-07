import aiohttp
import asyncio
import funcy
import sys
import time

async def fetch(url, session, max_redirects):
    async with session.request('GET', url, max_redirects=max_redirects) as response:
        return (response.url, response.status, await response.read())


async def send(token, chunk):
    max_redirects = len(chunk) * 8
    headers = { 'Authorization': f'Bearer {token}' }

    async with aiohttp.ClientSession(headers=headers) as session:
        st = time.time_ns()
        tasks = [asyncio.ensure_future(fetch(c, session, max_redirects)) for c in chunk]
        results = await asyncio.gather(*tasks)
        et = time.time_ns()
        print(f'{(et-st)/1000000}')
        statuses = [status for (url, status, text) in results]
        print('Chunk statuses: ', statuses)
        for (url, status, content) in results:
            if status == 500:
                print('--------------------------------')
                print(f'URL: {url}')
                print('Response content:')
                print(content)


async def main(token_fn, concurrent, url_fn):
    with open(token_fn, 'rt') as f:
        token = f.readline().strip()
    with open(url_fn, 'rt') as f:
        requests = f.readlines()

    print()
    print(f'Sending chunks of {concurrent} concurrent requests')

    for chunk in funcy.chunks(concurrent, requests):
        await send(token, chunk)


if __name__ == '__main__':
    token_fn = sys.argv[1]
    concurrent = int(sys.argv[2])
    url_fn = sys.argv[3]

    asyncio.run(main(token_fn, concurrent, url_fn))
