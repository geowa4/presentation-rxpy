#!/usr/bin/env python
import logging
import selectors
import socket
from functools import partial
import rx
from rx import Observable
asyncio = rx.config['asyncio']


def main():
    """Create your own."""

    logging.basicConfig(level=logging.DEBUG)

    # Parts taken from https://docs.python.org/3/library/selectors.html
    sel = selectors.DefaultSelector()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(sel, loop))
    try:
        while True:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
    except KeyboardInterrupt:
        pass
    loop.close()

    logging.info('closed event loop')


async def run(sel, loop):
    sock = socket.socket()
    sock.bind(('localhost', 1234))
    sock.listen(100)
    sock.setblocking(False)

    def create_socket_observable(observer):
        sel.register(
            sock,
            selectors.EVENT_READ,
            partial(accept, observer, sel)
        )

    source = Observable.create(
        create_socket_observable
    ).share()

    source.subscribe(
        logging.info
    )

    source.where(
        lambda msg: "error" in msg
    ).subscribe(
        logging.error
    )


def accept(observer, sel, sock, mask):
    conn, addr = sock.accept()  # Should be ready
    observer.on_next('accepted {} from {}'.format(conn, addr))
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, partial(read, observer, sel))


def read(observer, sel, conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        observer.on_next('echoing {} to {}'.format(repr(data), conn))
        conn.send(data)  # Hope it won't block
    else:
        observer.on_next('closing {}'.format(conn))
        sel.unregister(conn)
        conn.close()


if __name__ == '__main__':
    main()
