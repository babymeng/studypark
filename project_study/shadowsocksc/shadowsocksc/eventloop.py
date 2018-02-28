#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import socket
import select
import errno
import logging
from collections import defaultdict


__all__ = ['EventLoop', 'POLL_NULL', 'POLL_IN', 'POLL_OUT', 'POLL_ERR',
           'POLL_HUP', 'POLL_NVAL', 'EVENT_NAMES']

POLL_NULL = 0x00
POLL_IN   = 0x01
POLL_OUT  = 0x04
POLL_ERR  = 0x08
POLL_HUP  = 0x10
POLL_NAL  = 0x20


EVENT_NAMES = {
    POLL_NULL : 'POLL_NULL',
    POLL_IN   : 'POLL_IN',
    POLL_OUT  : 'POLL_OUT',
    POLL_ERR  : 'POLL_ERR',
    POLL_HUP  : 'POLL_HUP',
    POLL_NAL  : 'POLL_NAL',
}

class SelectSelector(object):
    def __init__(self, r_list, w_list, x_list):
        self._r_list = set()
        self._w_list = set()
        self._x_list = set()

    def poll(self, timeout):
        r, w, x = select.select(self._r_list, self._w_list, self._x_list, timeout)
        results = defaultdict(lambda: POLL_NULL)
        for p in [(r, POLL_IN), (w, POLL_OUT), (x, POLL_ERR)]:
            for fd in p[0]:
                results[fd] |= p[1]
        return results.items()
    
    def register(self, fd, mode):
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
    '''
    kqueue=select.kqueue()返回一个内核的queue object
    该kqueue拥有以下方法:
    1.kqueue.close()   Close the control file descriptor of the kqueue object.
                       关闭kqueue实例的控制文件描述符
    2.kqueue.closed    True if the kqueue object is close.
                       kqueue实例是否关闭
    3.kqueue.fileno()  Return the file descriptor number of the control fd.
                       返回返回控制文件的数字格式的文件描述符
    4.kqueue.fromfd(fd) Create a kqueue object from a given file descriptor.
                        从一个给定的文件描述符创建一个kqueue实例对象
    5.kqueue.control(changelist, max_events[, timeout=None]) -->eventlist.
                        返回一个事件列表（kevent事件）。用于开始监听并返回监听到的kevent
                  ·changelist must be an iterable of kevent object or None
                  ·max_events must be 0 or a positive integer
                  ·timeout in seconds (floats possible)
                  
    select.kevent(ident, filter=KQ_FILTER_READ, flags=KQ_EV_ADD, fflags=0, data=0, udata=0)Returns a kernel event object.返回一个（用于监听）内核event对象
    kevent事件内容:{kevent.ident:value, kevent.filter:value, kevent.flags:value, kevent.fflags:value, kevent.data:value, kevent.udata:value}
    kevent.ident: Value used to identify the event. The interpretation depends on the filter but it’s usually the file descriptor. In the constructor ident can either be an int or an object with a fileno() method. kevent stores the integer internally.它的值用来标识一个事件。它的解释依赖于filter，但通常代表文件描述符。
    kevent.filter: Name of the kernel filter. 内核过滤器的名称
    
    filter常量:
    Constant           Meaning
    KQ_FILTER_READ     Takes a descriptor and returns whenever there is data available to read
    KQ_FILTER_WRITE    Takes a descriptor and returns whenever there is data available to write
    KQ_FILTER_AIO      AIO requests
    KQ_FILTER_VNODE    Returns when one or more of the requested events watched in fflag occurs
    KQ_FILTER_PROC     Watch for events on a process id
    KQ_FILTER_NETDEV   Watch for events on a network device [not available on Mac OS X]
    KQ_FILTER_SIGNAL   Returns whenever the watched signal is delivered to the process
    KQ_FILTER_TIMER    Establishes an arbitrary timer
    kevent.flags: Filter action. 过滤器对应的执行动作
    flags常量包括:
    Constant       Meaning
    KQ_EV_ADD      Adds or modifies an event
    KQ_EV_DELETE   Removes an event from the queue
    KQ_EV_ENABLE   Permitscontrol() to returns the event
    KQ_EV_DISABLE  Disablesevent
    KQ_EV_ONESHOT  Removes event after first occurrence
    KQ_EV_CLEAR    Reset the state after an event is retrieved
    KQ_EV_SYSFLAGS internal event
    KQ_EV_FLAG1    internal event
    KQ_EV_EOF      Filter specific EOF condition
    KQ_EV_ERROR    See return values
    kevent.data: Filter specific data.

    [对于kqueue的操作,首先在循环之前调用kqueue.control([kevent], 0, 0)
    (把你的事件加入到监听队列当中,不去查询任何事件,立即返回),然后在循环时调用
    kequeue.control(None, size, timeout)来查询你的事件]
    '''
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
            if e.filter == select.KQ_FILTER_WRITE:
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

class EventLoop(object):
    def __init__(self):
        if hasattr(select, 'epoll'):
            self._impl  = select.epoll()
            model = 'epoll'
        elif hasattr(select, 'kqueue'):
            self._impl  = KqueueSelector()
            model = 'kqueue'
        elif hasattr(select, 'select'):
            self._impl  = SelectSelector()
            model = 'select'

        self._fdmap     = {}
        self._stopping  = False
        logging.debug('using event model: %s', model)

    def poll(self, timeout):
        events = self._impl.poll(timeout)
        return [(self._fdmap[fd][0], fd, event) for fd, event in events]

    def add(self, f, mode, handler):
        fd = f.fileno()
        self._fdmap[fd] = (f, handler)
        self._impl.register(fd, mode)

    def remove(self, f):
        fd = f.fileno()
        del self._fdmap[fd]
        self._impl.unregister(fd)

    def modify(self, f, mode):
        fd = f.fileno()
        self._impl.modify(fd, mode)

    def stop(self):
        self._stopping = True

    def run(self):
        events = []
        while not self._stopping:
            try:
                events = self.poll(10)
            except (OSError, IOError) as e:
                if errno_from_exception(e) in (errno.EPIPE, errno.EINTR):
                    logging.debug('poll:%s', e)
                else:
                    logging.error('poll:%s', e)
                    import traceback
                    traceback.print_exc()
                    continue

            for sock, fd, event in events:
                handler = self._fdmap.get(fd, None)
                if handler is not None:
                    handler = handler[1]
                    try:
                        handler.handle_event(sock, fd, event)
                    except (OSError, IOError) as e:
                        print(e)

            now = time.time()

    def close(self):
        self._impl.close()

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


# from tornado
def get_sock_error(sock):
    error_number = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
    return socket.error(error_number, os.strerror(error_number))

def main():
    print(KqueueSelector.__doc__)

if __name__ == '__main__':
    main()
