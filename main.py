from itertools import combinations_with_replacement
import string

import asyncio
import aiohttp


def nickname_generator(min_length: int, max_length: int):
    alphabet = ''.join(sorted(set(string.ascii_letters.lower()))) + string.digits
    for i in range(min_length, max_length + 1):
        for symbols in combinations_with_replacement(alphabet, i):
            yield ''.join(symbols)


async def get(url, sess):
    try:
        async with sess.get(url=url) as response:
            if response.status == 404:
                print(url)
    except Exception as e:
        pass


async def get_available_github_nicknames(min_length=2, max_length=3, threads=1):
    assert min_length <= max_length, f'{min_length=} must be <= {max_length=}'

    print('Available Github Nicknames\n')

    async with aiohttp.ClientSession() as sess:
        generator = nickname_generator(min_length, max_length)

        while True:
            try:
                urls = [f'https://github.com/{next(generator)}' for _ in range(threads)]

                await asyncio.gather(*[get(url, sess) for url in urls])
            except Exception as err:
                print(err)


def main():
    asyncio.run(get_available_github_nicknames(min_length=3, max_length=5, threads=50))


if __name__ == '__main__':
    main()
