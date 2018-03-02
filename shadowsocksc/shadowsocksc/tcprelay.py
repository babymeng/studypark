#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

        addrs = socket.getaddrinfo(listen_addr, listen_port, socket.AF_INAT,
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
            logging.info(logging.INFO, 'fd %d %s', fd,
                         eventloop.EVENT_NAMES.get(event, event))
        if sock == self._server_socket:
            if event & POLL_ERR:
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


class TCPRelayHandler(object):
    def __init__(self, server, fd_to_handlers, eventloop, local_sock, config,
                 dns_resolver, is_local):
        self._server            = server
        self._fd_to_handlers    = fd_to_handlers
        self._eventloop         = eventloop
        self._local_sock        = local_sock
        self._remote_sock       = remote_sock
        self._config            = config
        self._dns_resolver      = dns_resolver

        self._is_local          = is_local
        self._data_write_to_local   = []
        self._data_write_to_remote  = []
        self._client_address    = local_sock.getpeer()[:2]
        self._remote_address    = None

        fd_to_handlers[local_sock.fileno()] = self
        self._local_sock.setblocking(False)
        self._local_sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        
