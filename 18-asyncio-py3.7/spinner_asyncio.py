#!/usr/bin/env python

# spinner_asyncio.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN SPINNER_ASYNCIO
import asyncio
import itertools


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
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        print(status, flush=True, end='\r')
        try:
            await asyncio.sleep(.1)  # <2>
        except asyncio.CancelledError:  # <3>
            break
    print(' ' * len(status), end='\r')


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
    result = asyncio.run(supervisor())  # <11>
    print('Answer:', result)


if __name__ == '__main__':
    main()
# END SPINNER_ASYNCIO
