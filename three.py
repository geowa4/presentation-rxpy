#!/usr/bin/env python
import logging
import rx
from rx import Observable
from rx.concurrency import AsyncIOScheduler
asyncio = rx.config['asyncio']


def main():
    """Sharing is caring."""

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
    timer = Observable.timer(
        0,
        1000,
        scheduler=AsyncIOScheduler()
    ).tap(
        lambda t: logging.info('timer source ({})'.format(t))
    )

    timer.subscribe(
        logging.info
    )

    timer.select(
        lambda t: t * 2
    ).subscribe(
        logging.info
    )


if __name__ == '__main__':
    main()
