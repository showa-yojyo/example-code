#!/usr/bin/env python

# Inspired by
# https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/

import asyncio
import time

t0 = time.perf_counter()
hr = '─' * 50

async def countdown(label, delay):
    tabs = 6 * (ord(label) - ord('A')) * ' '
    for n in range(3, 0, -1):
        await asyncio.sleep(delay)
        dt = time.perf_counter() - t0
        print(hr)
        print(f'{dt:7.4f}s {tabs}{label} = {n}')

async def main():
    await asyncio.gather(
        *(countdown(i, j) for i, j in (
            ('A', .7),
            ('B', 2),
            ('C', .3),
            ('D', 1))))
    print('━' * 50)

if __name__ == '__main__':
    asyncio.run(main())
