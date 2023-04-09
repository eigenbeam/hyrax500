
import aiohttp
import asyncio
import funcy
import sys
import time
import random

save_sample_rate = 2    # percent 1 to 100
max_failures = 100
repeat = True


def random_true(percent_true):
    """ Return True percent_true of the time """
    return random.random() < percent_true / 100


def save_content(content, name):
    """ Save the content in a file """
    with open(name, 'wb') as f:
            f.write(content)


async def fetch(url, session, max_redirects):
    async with session.request('GET', url, max_redirects=max_redirects) as response:
        return (response.url, response.status, await response.read())


async def send(token, chunk, file_name):
    max_redirects = len(chunk) * 16
    headers = { 'Authorization': f'Bearer {token}', 'Accepts': 'deflate' }

    async with aiohttp.ClientSession(headers=headers) as session:
        st = time.time_ns()
        tasks = [asyncio.ensure_future(fetch(c, session, max_redirects)) for c in chunk]
        results = await asyncio.gather(*tasks)
        et = time.time_ns()
        print(f'Time to gather {len(chunk)} responses: {(et-st)/1000000} ms')     # Print time in ms
        statuses = [url for (url, status, text) in results]
        print('Chunk statuses: ', statuses)
        for (url, status, content) in results:
            if status == 500:
                print('--------------------------------')
                print(f'URL: {url}')
                print('Response content:')
                print(content)

            if status != 200:
                global failures
                failures += 1
                print('--------------------------------')
                print(f'URL: {url}')
                print(f'Response status: {status}')
                save_content(content, f'error_{failures}')
                if failures > max_failures:
                    sys.exit("Too many failures!")
            else:
                # only save if 'file_name' is not empty and either every response should
                # be saved or
                if file_name != '' and random_true(save_sample_rate):
                    global run_number
                    global file_number
                    file_number += 1
                    save_content(content, f'{file_name}_{run_number}_{file_number}')


async def main(token_fn, concurrent, url_fn, file_name):
    with open(token_fn, 'rt') as f:
        token = f.readline().strip()
    with open(url_fn, 'rt') as f:
        requests = f.readlines()

    print()
    print(f'Sending chunks of {concurrent} concurrent requests')

    for chunk in funcy.chunks(concurrent, requests):
        await send(token, chunk, file_name)


if __name__ == '__main__':
    token_fn = sys.argv[1]
    concurrent = int(sys.argv[2])
    url_fn = sys.argv[3]

    # If file_name is given, save the responses in numbered files, otherwise don't save them
    file_name = ""
    if len(sys.argv) == 5:
        file_name = sys.argv[4]

    run_number = 0
    file_number = 0     # file_number is a global
    failures = 0        # failures is global

    while repeat:
        run_number += 1
        try:
            asyncio.run(main(token_fn, concurrent, url_fn, file_name))

        except aiohttp.client_exceptions.TooManyRedirects as e:
            info = f'Too many redirects: {e}'
            print(info)
            save_content(bytes(info, 'ascii'), f'client_error_{run_number}')
        except aiohttp.client_exceptions.ServerDisconnectedError as e:
            info = f'Server Disconnected: {e}'
            print(info)
            save_content(bytes(info, 'ascii'), f'client_error_{run_number}')
        except aiohttp.client_exceptions.ClientOSError as e:
            info = f'Client OS Error: {e}'
            print(info)
            save_content(bytes(info, 'ascii'), f'client_error_{run_number}')

    if not repeat:
        asyncio.run(main(token_fn, concurrent, url_fn, file_name))
