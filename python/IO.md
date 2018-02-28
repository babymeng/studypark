Python中的select模块专注于I/O多路复用，提供了select/poll/epoll三个方法(windows/linux/linux)，另外也提供了kqueue方法(freeBSD系统)<br>

### **select方法**   
_select.select()进程指定内核监听哪些文件描述符的事件(最多1024个文件描述符fd),当没有文件描述符事件发生时,进程被阻塞;当一个或多个文件描述符事件发生时,进程被唤醒_ 
``` 
当调用select()时:  
1. 上下文切换为内核态
2. 将fd从用户空间复制到内核空间
3. 内核遍历所有fd,查看其对应事件是否发生
4. 如果没有发生,将进程阻塞,当设备驱动产生终端或者timeout时间后，将进程唤醒，再次进行遍历
5. 返回遍历后的fd
6. 将fd从内核空间复制到用户空间
```  
```
fd_r_list, fd_w_list, fd_e_list = select.select(rlist, wlist, xlist, [timeout])  
参数： 可接受四个参数（前三个必须）  
rlist: wait until ready for reading，即我们需要内核监听的读文件描述符列表，当读事件触发时，返回对应的文件描述符列表  
wlist: wait until ready for writing，即我们需要内核监听的写文件描述符列表，当写事件触发时，返回对应的文件描述符列表  
xlist: wait for an “exceptional condition”   
timeout: 超时时间   
返回值：三个列表   
select方法用来监视文件描述符(当文件描述符条件不满足时，select会阻塞)，当某个文件描述符状态改变后，会返回三个列表   
1、当参数1 序列中的fd满足“可读”条件时，则获取发生变化的fd并添加到fd_r_list中 
2、当参数2 序列中含有fd时，则将该序列中所有的fd添加到 fd_w_list中   
3、当参数3 序列中的fd发生错误时，则将该发生错误的fd添加到 fd_e_list中  
4、当超时时间为空，则select会一直阻塞，直到监听的句柄发生变化;当超时时间 ＝ n(正整数)时，那么如果监听的句柄均无任何变化，
则select会阻塞n秒，之后返回三个空列表，如果监听的句柄有变化，则直接执行。   
```
select弊端:   
_1.当文件描述符过多时，文件描述符在用户空间与内核空间进行copy会很费时_  
_2.当文件描述符过多时，内核对文件描述符的遍历也很浪费时间_  
_3.select最大仅仅支持1024个文件描述符_   
eg:   
server端  
```python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import socket
import select

def select_server():
    listen_addr = '127.0.0.1'
    listen_port = 1083
    addrs = socket.getaddrinfo(listen_addr, listen_port, 0, socket.SOCK_STREAM, socket.SOL_TCP)
    af, socktype, proto, canonname, sockaddr = addrs[0]
    
    server = socket.socket(af, socktype, proto)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(sockaddr)
    server.setblocking(False)
    server.listen(1024)

    r_list = [server,]
    w_list = []
    x_list = []
    num    = 0
    stopping = False

    while not stopping:
        num += 1
        print("num:", num)
        rlist, wlist, xlist = select.select(r_list, w_list, x_list, 10)
        print("r_list:", r_list)
        print("rlist:", rlist)

        for sock in rlist:
            if sock == server:
                conn, addr = sock.accept()
                r_list.append(conn)
            else:
                msg = sock.recv(1024)
                print('msg:', msg)
                if not msg:
                    r_list.remove(sock)
        
    server.close()
if __name__ == '__main__':
    select_server()
```
client端  
```python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import socket
import time

def select_client():
    server_addrs = ('127.0.0.1', 1083)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_addrs)
    time.sleep(1)
    
    msg = b"Hello:I'm client!"
    client.send(msg)
    
    time.sleep(1)
    client.close()
                
if __name__ == '__main__':
    select_client()
```
### epoll方法：

select.epoll()方法  
_1.epoll的解决方案在epoll_ctl函数中。每次注册新的事件到epoll句柄中时，会把所有的fd拷贝进内核，而不是在epoll_wait的时候重复拷贝.epoll保证了每个fd在整个过程中只会拷贝一次._  
_2.epoll会在epoll_ctl时把指定的fd遍历一遍（这一遍必不可少）并为每个fd指定一个回调函数，当设备就绪，唤醒等待队列上的等待者时，就会调用这个回调函数，而这个回调函数会把就绪的fd加入一个就绪链表。epoll_wait的工作实际上就是在这个就绪链表中查看有没有就绪的fd_  
_3.epoll对文件描述符没有额外限制_  
```
select.epoll(sizehint=-1, flags=0) 创建epoll对象
1.epoll.close()   Close the control file descriptor of the epoll object.关闭epoll对象的文件描述符
2.epoll.closed    True if the epoll object is closed.检测epoll对象是否关闭
3.epoll.fileno()  Return the file descriptor number of the control fd.返回epoll对象的文件描述符
4.epoll.fromfd(fd)Create an epoll object from a given file descriptor.根据指定的fd创建epoll对象
5.epoll.register(fd[, eventmask]) Register a fd descriptor with the epoll object.向epoll对象中注册fd和对应的事件
6.epoll.modify(fd, eventmask)  Modify a registered file descriptor.修改fd的事件
7.epoll.unregister(fd) Remove a registered file descriptor from the epoll object.取消注册
8.epoll.poll(timeout=-1, maxevents=-1)Wait for events. timeout in seconds (float)阻塞，直到注册的fd事件发生,会返回一个dict，格式为：{(fd1,event1),(fd2,event2),……(fdn,eventn)}
EPOLL 事件
EPOLLIN     Available for read 可读   状态符为1
EPOLLOUT    Available for write 可写  状态符为4
EPOLLPRI    Urgent data for read
EPOLLERR    Error condition happened on the assoc. fd 发生错误 状态符为8
EPOLLHUP    Hang up happened on the assoc. fd 挂起状态
EPOLLET     Set Edge Trigger behavior, the default is Level Trigger behavior 默认为水平触发，设置该事件后则边缘触发
EPOLLONESHOT    Set one-shot behavior. After one event is pulled out, the fd is internally disabled
EPOLLRDNORM    Equivalent to EPOLLIN
EPOLLRDBAND    Priority data band can be read.
EPOLLWRNORM    Equivalent to EPOLLOUT
EPOLLWRBAND    Priority data may be written.
EPOLLMSG       Ignored.
```
### 水平触发和边缘触发
##### Level_triggered(水平触发，有时也称条件触发)
当被监控的文件描述符上有可读写事件发生时，epoll.poll()会通知处理程序去读写。如果这次没有把数据一次性全部读写完(如读写缓冲区太小)，那么下次调用 epoll.poll()时，它还会通知你在上没读写完的文件描述符上继续读写，当然如果你一直不去读写，它会一直通知你！！！如果系统中有大量你不需要读写的就绪文件描述符，而它们每次都会返回，这样会大大降低处理程序检索自己关心的就绪文件描述符的效率！！！ 优点很明显：稳定可靠   
##### Edge_triggered(边缘触发，有时也称状态触发)
当被监控的文件描述符上有可读写事件发生时，epoll.poll()会通知处理程序去读写。如果这次没有把数据全部读写完(如读写缓冲区太小)，那么下次调用epoll.poll()时，它不会通知你，也就是它只会通知你一次，直到该文件描述符上出现第二次可读写事件才会通知你！！！这种模式比水平触发效率高，系统不会充斥大量你不关心的就绪文件描述符！！！缺点：某些条件下不可靠   
eg:(在下macos,只测试了select()和kqueue(),不支持epoll())  
server  
```python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import socket
import select

def epoll_server():
    listen_addr = '127.0.0.1'
    listen_port = 1083
    addrs = socket.getaddrinfo(listen_addr, listen_port, 0, socket.SOCK_STREAM, socket.SOL_TCP)
    af, socktype, proto, canonname, sockaddr = addrs[0]
    
    server = socket.socket(af, socktype, proto)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(sockaddr)
    server.setblocking(False)
    server.listen(1024)

    epoll_obj = select.epoll()
    epoll_obj.register(server.fileno(), select.EPOLLIN)

    events = []
    conns  = []
    stopping = False
    while not stopping:
        try:
            events = epoll_obj.poll(10)
        except (OSError, IOError) as e:
            print("poll:", e)
            continue

        for fd, event in events:
            if fd == server.fileno():
                conn, addr = server.accept()
                epoll_obj.register(conn.fileno(), select.EPOLLIN | select.EPOLLOUT)
                conns[conn.fileno()] = conn
            else:
                try:
                    msg = sock.recv(1024)
                    print('msg:', msg)
                except BrokenPipeError :
                    epoll_obj.unregister(fd)
                    conns[fd].close()
                    del conns[fd]
        
    server.close()
                
if __name__ == '__main__':
    epoll_server()
```
### kqueue方法：
kqueue=select.kqueue()返回一个内核的queue object  
该kqueue拥有以下方法:  
```
1.kqueue.close() Close the control file descriptor of the kqueue object. 关闭kqueue实例的控制文件描述符
2.kqueue.closed  True if the kqueue object is close. kqueue实例是否关闭
3.kqueue.fileno() Return the file descriptor number of the control fd.返回返回控制文件的数字格式的文件描述符
4.kqueue.fromfd(fd) Create a kqueue object from a given file descriptor. 从一个给定的文件描述符创建一个kqueue实例对象
5.kqueue.control(changelist, max_events[, timeout=None]) -->eventlist. 返回一个事件列表（kevent事件）。用于开始监听并返回监听到的kevent
      changelist: must be an iterable of kevent object or None
      max_events: must be 0 or a positive integer
      timeout   : in seconds (floats possible)
select.kevent(ident, filter=KQ_FILTER_READ, flags=KQ_EV_ADD, fflags=0, data=0, udata=0)Returns a kernel event object.返回一个（用于监听）内核event对象
kevent事件内容:{kevent.ident:value, kevent.filter:value, kevent.flags:value, kevent.fflags:value,kevent.data:value, kevent.udata:value}
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
kevent.udata: User defined value.
```
_**对于kqueue的操作,也许只需要通过你想要的kevent列表来改变queue队列,首先在循环之前调用kqueue.control([kevent], 0, 0)(把你的事件加入到监听队列当中,不去查询任何事件,立即返回),然后在循环时调用kequeue.control(None, size, timeout)来查询你的事件.**_  

eg:  
server  
```python
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
        #elif hasattr(select, 'select'):
            #self._impl = SelectSelector()
            #model = 'select'

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
```
