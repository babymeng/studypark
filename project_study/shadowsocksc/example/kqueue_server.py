#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import socket
import select
from collections import defaultdict
import logging

POLL_NULL   = 0x00
POLL_IN     = 0x01
POLL_OUT    = 0x04
POLL_ERR    = 0x08
POLL_HUP    = 0x10

class SelectSelector(object):
    MAX_EVENTS = 1024

    def __init__(self):
        self._r_list = set()
        self._w_list = set()
        self._x_list = set()

    def poll(self, timeout=None):
        r, w, x = select.select(self._r_list, self._w_list, self._x_list, timeout)
        results = defaultdict(lambda: POLL_NULL)
        for p in [(r, POLL_IN), (w, POLL_OUT), (x, POLL_ERR)]:
            for fd in p[0]:
                results[fd] |= p[1]
        return results.items()

    def register(self, f, mode):
        if mode & POLL_IN:
            self._r_list.add(fd)
        if mode & POLL_OUT:
            self._w_list.add(fd)
        if mode & POLL_ERR:
            self._x_list.add(fd)

    def unregister(self, fd):
        if fd in self._r_list:
            self._r_list.remove(fd)
        if fd in self._w_list:
            self._w_list.remove(fd)
        if fd in self._x_list:
            self._x_list.remove(fd)

    def modify(self, fd, mode):
        self.unregister(fd)
        self.register(fd, mode)

    def close(self):
        pass
    
class KqueueSelector(object):
    MAX_EVENTS = 1024

    def __init__(self):
        self._kqueue = select.kqueue()
        self._fds    = {}

    def _control(self, fd, mode, flags):
        events = []
        if mode & POLL_IN:
            events.append(select.kevent(fd, select.KQ_FILTER_READ, flags))
        if mode & POLL_OUT:
            events.append(select.kevent(fd, select.KQ_FILTER_WRITE, flags))
        for e in events:
            self._kqueue.control([e], 0)

    def poll(self, timeout):
        if timeout < 0:
            timeout = None

        events = self._kqueue.control(None, KqueueSelector.MAX_EVENTS, timeout)
        results = defaultdict(lambda: POLL_NULL)
        for e in events:
            fd = e.ident
            if e.filter == select.KQ_FILTER_READ:
                results[fd] |= POLL_IN
            elif e.filter == select.KQ_FILTER_WRITE:
                results[fd] |= POLL_OUT
        return results.items()
            
    def register(self, fd, mode):
        self._fds[fd] = mode
        self._control(fd, mode, select.KQ_EV_ADD)

    def unregister(self, fd):
        self._control(fd, self._fds[fd], select.KQ_EV_DELETE)
        del self._fds[fd]

    def modify(self, fd, mode):
        self.unregister(fd)
        self.register(fd, mode)

    def close(self):
        self._kqueue.close()
        
# from tornado
def errno_from_exception(e):
    """Provides the errno from an Exception object.

    There are cases that the errno attribute was not set so we pull
    the errno out of the args but if someone instatiates an Exception
    without any args you will get a tuple error. So this function
    abstracts all that behavior to give you a safe way to get the
    errno.
    """

    if hasattr(e, 'errno'):
        return e.errno
    elif e.args:
        return e.args[0]
    else:
        return None
    
def create_server():
    listen_addr = '127.0.0.1'
    listen_port = 1083
    addrs = socket.getaddrinfo(listen_addr, listen_port, 0, socket.SOCK_STREAM, socket.SOL_TCP)
    af, socktype, proto, canonname, sockaddr = addrs[0]
    
    server = socket.socket(af, socktype, proto)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(sockaddr)
    server.setblocking(False)
    server.listen(1024)

    return server

class EventLoop(object):
    def __init__(self):
        if hasattr(select, 'epoll'):
            self._impl = select.epoll()
            model = 'epoll'
        elif hasattr(select, 'kqueue'):
            self._impl = KqueueSelector()
            model = 'kqueue'
        elif hasattr(select, 'select'):
            self._impl = SelectSelector()
            model = 'select'

        self._fdmap     = {}
        self._stopping  = False
        logging.debug('using event model: %s', model)

    def poll(self, timeout=None):
        events = self._impl.poll(timeout)
        return [(self._fdmap[fd], fd, event) for fd, event in events]

    def add(self, f, mode, handler):
        fd = f.fileno()
        self._fdmap[fd] = (f, handler)
        self._impl.register(fd, mode)

    def move(self, f):
        fd = f.fileno()
        del self._fdmap[fd]
        self._impl.unregister(fd, mode)

    def modify(self, f, mode):
        fd = f.fileno()
        self._impl.modify(f, mode)

    def run(self):
        server = create_server()
        fd = server.fileno()
        self._impl = KqueueSelector()
        self._fdmap[fd] = server
        self._impl.register(fd, POLL_IN)

        events = []
        while(not self._stopping):
            try:
                events = self._impl.poll(10)
                logging.debug("events:%s", events)
            except (IOError, OSError) as e:
                if errno_from_exception(e) in (errno.EPIPE, errno.EINTR):
                    # EPIPE: Happens when the client closes the connection
                    # EINTR: Happens when received a signal
                    # handles them as soon as possible
                    logging.debug("epoll_exception e:%d", errno_from_exception(e))
                else:
                    import traceback
                    traceback.print_exc()
                    continue

            for fd, event in events:
                if fd == server.fileno():
                    conn, addr = server.accept()
                    self._fdmap[conn.fileno()] = (conn, None)
                    self._impl.register(conn.fileno(), POLL_IN)
                else:
                    if event == POLL_IN:
                        msg = self._fdmap[fd][0].recv(1024)
                        logging.debug("msg:%s", msg)
                        if b'\n\n' == msg:
                            self._impl.unregister(fd)
                            logging.debug("unregister fd:%d", fd)
                    elif event == POLL_OUT:
                        self._fdmap[fd][0].send(b'Hello Client!')
                        logging.debug("Hello Client!")
                    else:
                        logging.debug("unknow event:%d", event)

        server.close()
                
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(lineno)-4d %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    EventLoop().run()
