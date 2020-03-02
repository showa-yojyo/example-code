"""
A coroutine to compute a running average

# BEGIN CORO_AVERAGER_TEST
    >>> coro_avg = averager()  # <1>
    >>> next(coro_avg)  # <2>
    >>> coro_avg.send(10)  # <3>
    10.0
    >>> coro_avg.send(30)
    20.0
    >>> coro_avg.send(5)
    15.0

# END CORO_AVERAGER_TEST
"""

import asyncio

# BEGIN CORO_AVERAGER
@asyncio.coroutine
def averager():
    """ A generator-based coroutine

    >>> import inspect
    >>> inspect.isgeneratorfunction(averager)
    True
    >>> import asyncio
    >>> asyncio.iscoroutinefunction(averager)
    True
    >>> a = averager()
    >>> inspect.isgenerator(a)
    True
    >>> asyncio.iscoroutine(a)
    True
    """

    total = 0.0
    count = 0
    average = None
    while True:  # <1>
        term = yield average  # <2>
        total += term
        count += 1
        average = total/count
# END CORO_AVERAGER
