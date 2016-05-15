#!/usr/bin/env python
import logging
import rx
asyncio = rx.config['asyncio']


def main():
    """Somewhat simple example of asyncio"""

    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_something())
    loop.close()

    logging.info('closed event loop')


async def do_something():
    logging.info('doing something')
    await asyncio.sleep(2)
    val = await do_something_else()
    logging.info('did something and got {}'.format(val))


async def do_something_else():
    await asyncio.sleep(5)
    return 7

if __name__ == '__main__':
    main()
