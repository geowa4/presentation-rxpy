#!/usr/bin/env python
import logging
import rx
from rx import Observable
from rx.concurrency import AsyncIOScheduler
asyncio = rx.config['asyncio']


def main():
    """Simple example of Rx Timer"""

    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    loop.close()

    logging.info('closed event loop')


async def run(loop):
    Observable.timer(
        0,
        1000,
        scheduler=AsyncIOScheduler()
    ).tap(
        logging.info
    )


if __name__ == '__main__':
    main()
