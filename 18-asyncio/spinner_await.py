#!/usr/bin/env python

# spinner_await.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

import asyncio
import itertools
import sys


async def spin(msg):  # <1>
    """A native coroutine
    >>> import inspect
    >>> inspect.isgeneratorfunction(spin)
    False
    >>> inspect.iscoroutinefunction(spin)
    True
    >>> asyncio.iscoroutinefunction(spin)
    True
    """
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)  # <2>
        except asyncio.CancelledError:  # <3>
            break
    write(' ' * len(status) + '\x08' * len(status))


async def slow_function():  # <4>
    """A native coroutine
    >>> import inspect
    >>> inspect.isgeneratorfunction(slow_function)
    False
    >>> inspect.iscoroutinefunction(slow_function)
    True
    >>> asyncio.iscoroutinefunction(slow_function)
    True
    """
    # pretend waiting a long time for I/O
    await asyncio.sleep(3)  # <5>
    return 42


async def supervisor():  # <6>
    """A native coroutine
    >>> import inspect
    >>> inspect.isgeneratorfunction(supervisor)
    False
    >>> inspect.iscoroutinefunction(supervisor)
    True
    >>> asyncio.iscoroutinefunction(supervisor)
    True
    """
    spinner = asyncio.create_task(spin('thinking!'))  # <7>
    print('spinner object:', spinner)  # <8>
    result = await slow_function()  # <9>
    spinner.cancel()  # <10>
    return result


def main():
    result = asyncio.run(supervisor())  # <12>
    print('Answer:', result)


if __name__ == '__main__':
    main()
