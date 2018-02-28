#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import eventloop
import logging
import common
import struct

# we clear at most TIMEOUTS_CLEAN_SIZE timeouts each time
TIMEOUTS_CLEAN_SIZE = 512

# socks command definations
CMD_CONNECT   = 1
CMD_BIND      = 2
CMD_ASSOCIATE = 3

# for each opening port, we have a TCP Relay

# for each connection, we have a TCP Relay Handler to handle the connection

# for each handler, we have 2 sockets:
#   local:  connected to the client
#   remote: connected to the remote server

# for each handler, it could be at one of several stages:

# as sslocal:
# stage 0 SOCKS hello recv from local, send hello to local client
# stage 1 addr received from local client, query DNS for remote
# stage 2 UDP assoc
# stage 3 DNS resolved, connect to remote
# stage 4 still connecting, more data received from local
# stage 5 remote conected, piping local and remote

# as ssserver:
# stage 0 just jump to stage 1
# stage 1 addr received from local, query DNS for remote
# stage 3 DNS resolved, connect to remote
# stage 4 still connecting, more data received from local
# stage 5 remote connected, piping local and remote

STAGE_INIT = 0
STAGE_ADDR = 1
STAGE_UDP_ASSOC = 2
STAGE_DNS = 3
STAGE_CONNECTING = 4
STAGE_STREAM = 5
STAGE_DESTROYED = -1

# for each handler, we have 2 stream directions:
#   upstream:   from client to server direction
#               read local and write to remote
#   downstream: from server to client direction
#               read remote and write to local

STREAM_UP = 0
STREAM_DOWN = 1

# for each stream, it's waiting for reading, or writing, or both
WAIT_STATUS_INIT = 0
WAIT_STATUS_READING = 1
WAIT_STATUS_WRITING = 2
WAIT_STATUS_RDWRING = WAIT_STATUS_READING | WAIT_STATUS_WRITING

BUF_SIZE = 32 * 1024

NEGO_METHODS = {
    0   :'NO_AUTHENTICATION',
    1   :'GSSAPI',
    2   :'USERNAME_PASSWORD',
    3   :'IANA_ASSIGNED',
    4   :'PRI_METHOD',
    255 :'NO_ACCEPTABLE',
    }

class TCPRelay(object):
    def __init__(self, config, dns_resolver, is_local):
        self._config        = config
        self._dns_resolver  = dns_resolver
        self._is_local      = is_local
        self._closed        = False
        self._eventloop     = None
        self._fd_to_handlers= {}

        if is_local:
            listen_addr     = config['local_address']
            listen_port     = config['local_port']
        else:
            listen_addr     = config['server']
            listen_port     = config['server_port']
        self._listen_port   = listen_port

        addrs = socket.getaddrinfo(listen_addr, listen_port, socket.AF_INET,
                                   socket.SOCK_STREAM, socket.SOL_TCP)
        if len(addrs) == 0:
            raise Exception("can't get addrinfo for %s %d" %
                            (listen_addr, listen_port))
        af, socktype, proto, cannoname, sockaddr = addrs[0]
        server_socket = socket.socket(af, socktype, proto)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(sockaddr)
        server_socket.setblocking(False)
        server_socket.listen(1024)

        self._server_socket = server_socket
        print('server_socket:', server_socket)

    def add_to_loop(self, loop):
        if self._eventloop:
            raise Exception("already add to loop.")
        if self._closed:
            raise Exception('already closed.')

        self._eventloop = loop
        self._eventloop.add(self._server_socket,
                            eventloop.POLL_IN | eventloop.POLL_ERR, self)

    def handle_event(self, sock, fd, event):
        if sock:
            logging.log(5, 'fd %d %s', fd,
                         eventloop.EVENT_NAMES.get(event, event))
        if sock == self._server_socket:
            if event & eventloop.POLL_ERR:
                raise Exception("server socket error.")
            try:
                conn = self._server_socket.accept()
                TCPRelayHandler(self, self._fd_to_handlers,
                                self._eventloop, conn[0], self._config,
                                self._dns_resolver, self._is_local)
            except (OSError, IOError) as e:
                print("e", e)
        else:
            if sock:
                handler = self._fd_to_handlers.get(fd, None)
                if handler:
                    handler.handle_event(sock, event)
            else:
                logging.warn('poll removed fd')

    def close(self, next_tick=False):
        logging.debug('TCP close')
        self._closed = True
        if not next_tick:
            if self._eventloop:
                self._eventloop.remove(self._server_socket)
        self._server_socket.close()
        for handler in list(self._fd_to_handlers.values()):
            handler.destroy()
                

class TCPRelayHandler(object):
    def __init__(self, server, fd_to_handlers, eventloop, local_sock, config,
                 dns_resolver, is_local):
        self._server            = server
        self._fd_to_handlers    = fd_to_handlers
        self._eventloop         = eventloop
        self._local_sock        = local_sock
        self._remote_sock       = None
        self._config            = config
        self._dns_resolver      = dns_resolver

        self._is_local          = is_local
        self._stage             = STAGE_INIT
        self._data_write_to_local   = []
        self._data_write_to_remote  = []
        self._upstream_status   = WAIT_STATUS_READING
        self._downstream_status = WAIT_STATUS_INIT
        self._client_address    = local_sock.getpeername()[:2]
        self._remote_address    = None
        if is_local:
            self._chosen_server = self._get_a_server()

        fd_to_handlers[local_sock.fileno()] = self
        self._local_sock.setblocking(False)
        self._local_sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        #self._eventloop.add(local_sock, eventloop.POLL_IN | eventloop.POLL_ERR, self._server)
        self._eventloop.add(local_sock, 1 | 4, self._server)

    def _get_a_server(self):
        server = self._config['server']
        server_port = self._config['server_port']
        if type(server) == list:
            server = random.choice(server)
        if type(server_port) == list:
            server_port = random.choice(server_port)
        logging.debug('chosen server: %s %d', server, server_port)
        return server, server_port

    def handle_event(self, sock, event):
        if sock == self._remote_sock:
            pass
        elif sock == self._local_sock:
            if event & eventloop.POLL_ERR:
                #do error thing
                pass
            if event & (eventloop.POLL_IN | eventloop.POLL_HUP):
                self._on_local_read()
            if event & eventloop.POLL_OUT:
                #self._on_local_write()
                pass
        else:
            logging.warn('unknow socket.')

    def _nego_socks(self, data):
        logging.debug('recv client nego data: %s', data)
        #data:b'\x05\x02\x00\x02'
        ver = data[0]
        nmethod = data[1]
        methods = list(data[2:])
        refuse  = True

        if ver != 5:
            ret_exit = True
        logging.debug('VERSION: %d', ver)

        for num in methods:
            #print("METHOD: ", num, " ", NEGO_METHODS[num])
            logging.debug('METHOD: %d %s', num, NEGO_METHODS[num])
            if num == 0:
                refuse = False

        if not refuse:
            self._write_to_sock(b'\x05\x00', self._local_sock)
        else:
            self._write_to_sock(b'\x05\xff', self._local_sock)
            self.destroy()
        return refuse

    def _on_local_read(self):
        if not self._local_sock:
            return
        is_local = self._is_local
        data = None
        try:
            data = self._local_sock.recv(BUF_SIZE)
            logging.info("data recv: %s" % data)
        except (OSError, IOError) as e:
            if eventloop.errno_from_exception(e) in (errno.ETIMEOUT, errno.EAGAIN, errno.EWOULDBLOCK):
                return

        if not data:
            self.destroy()
            return
        if not is_local:
            #decrypt data
            logging.info('decrpt data')
        if self._stage == STAGE_STREAM:
            if self._is_local:
                #encrypt data
                logging.info('encrypt data')
            self._write_to_sock(data, self._remote_sock)
            return
        elif is_local and self._stage == STAGE_INIT:
            if self._nego_socks(data):
                logging.error('nego failed.')
                return
            self._stage = STAGE_ADDR
            return
        elif self._stage == STAGE_CONNECTING:
            #self._handle_stage_connecting(data)
            pass
        elif (is_local and self._stage == STAGE_ADDR) or \
                (not is_local and self._stage == STAGE_INIT):
            self._handle_stage_addr(data)

    def _write_to_sock(self, data, sock):
        if not data or not sock:
            return False
        uncomplete = False
        try:
            l = len(data)
            s = sock.send(data)
            if s < l:
                data = data[s:]
                uncomplete = True
        except (OSError, IOError) as e:
            error_no = eventloop.errno_from_exception(e)
            if error_no in (errno.EAGAIN, errno.EINPROGRESS,
                            errno.EWOULDBLOCK):
                uncomplete = True
            else:
                print('e:', e)
                self.destroy()
                return False
        if uncomplete:
            if sock == self._local_sock:
                self._data_write_to_local.append(data)
                #trigger STREAM_DOWN status
                self._update_stream(STREAM_DOWN, WAIT_STATUS_WRITING)
            elif sock == self._remote_sock:
                self._data_write_to_remote.append(data)
                #trigger STREAM_UP status
                self._update_stream(STREAM_UP, WAIT_STATUS_WRITING)
            else:
                logging.error('write_all_to_socket: unknow socket.')
        else:
            if sock == self._local_sock:
                #trigger STREAM_DOWN status
                self._update_stream(STREAM_DOWN, WAIT_STATUS_READING)
            elif sock == self._remote_sock:
                #trigger STREAM_UP status
                self._update_stream(STREAM_UP, WAIT_STATUS_READING)
            else:
                logging.error('write_all_to_socket: unknow socket.')
        return True

    def _update_stream(self, stream, status):
        dirty = False
        if status == STREAM_DOWN:
            if self._downstream_status != status:
                self._downstream_status = status
                dirty = True
        elif status == STREAM_UP:
            if self._upstream_status != status:
                self._upstream_status = status
                dirty = True

        if dirty:
            if self._local_sock:
                event = eventloop.POLL_ERR
                if self._downstream_status & WAIT_STATUS_WRITING:
                    event |= eventloop.POLL_OUT
                if self._upstream_status & WAIT_STATUS_READING:
                    event |= eventloop.POLL_IN
                self._eventloop.modify(self._local_sock, event)
            if self._remote_sock:
                event = eventloop.POLL_ERR
                if self._downstream_status & WAIT_STATUS_READING:
                    event |= eventloop.POLL_IN
                if self._upstream_status & WAIT_STATUS_WRITING:
                    event |= eventloop.POLL_OUT
                self._eventloop.modify(self._remote_sock, event)

    def _handle_stage_addr(self, data):
        try:
            if self._is_local:
                cmd = common.ord(data[1])
                if cmd == CMD_ASSOCIATE:
                    logging.debug('UDP associate.')
                    if self._local_sock.family == socket.AF_INET6:
                        header = b'\x05\x00\x00\x04'
                    elif self._local_sock.family == socket.AF_INET:
                        header = b'\x05\x00\x00\x01'
                    addr, port = self._local_sock.getsockname()[:2]
                    logging.debug('local_sock:%s %d', addr, port)
                    addr_to_send = common.inet_hton(self._local_sock.family, addr)
                    port_to_send = struct.pack('>H', port)
                    self._write_to_sock(header + addr_to_send + port_to_send, self._local_sock)
                    self._stage = STAGE_UDP_ASSOC
                    return
                elif cmd == CMD_CONNECT:
                    data = data[3:]
                else:
                    logging.error('unsupported command %d', cmd)
                    self.destroy()
                    return
                header_result = common.parse_header(data)
                logging.info('header_result: %s', header_result)
                if header_result is None:
                    raise Exception('can not parse header')
                addrtype, remote_addr, remote_port, header_length = header_result
                logging.info('connecting %s:%d from %s:%d' %
                             (common.to_str(remote_addr), remote_port,
                              self._client_address[0], self._client_address[1]))
                self._remote_address = (common.to_str(remote_addr), remote_port)
                self._update_stream(STREAM_UP, WAIT_STATUS_WRITING)
                self._stage = STAGE_DNS
                if self._is_local:
                    self._write_to_sock(b'\x05\x00\x00\x01\x00\x00\x00\x00\x10\x10',
                                        self._local_sock)
                    #data_to_send = self._encrptor.encrpt(data)
                    self._data_write_to_remote.append(data)
                    self._dns_resolver.resolve(self._chosen_server[0],
                                               self._handle_dns_resolved)
        except (OSError, IOError) as e:
            pass

    def destroy(self):
        if self._stage == STAGE_DESTROYED:
            return
        self._stage = STAGE_DESTROYED

        if self._remote_sock:
            self._eventloop.remove(self._remote_sock)
            del self._fd_to_handlers[self._remote_sock.fileno()]
            self._remote_sock.close()
            self._remote_sock = None
        if self._local_sock:
            self._eventloop.remove(self._local_sock)
            del self._fd_to_handlers[self._local_sock.fileno()]
            self._local_sock.close()
            self._local_sock = None
