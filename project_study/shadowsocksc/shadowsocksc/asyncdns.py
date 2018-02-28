#/usr/bin/env python
# -*- coding: utf-8 -*-

import common
import socket
import logging


class DNSResolver(object):
    def __init__(self):
        self._loop = None
        self._hosts = {}
        self._hostname_status = {}
        self._hostname_to_cb = {}
        self._cb_to_hostname = {}
        self._sock = None
        self._servers = None
        self._parse_resolv()
        self._parse_hosts()

    def _parse_resolv(self):
        self._servers = []
        try:
            with open('/etc/resolv.conf', 'rb') as f:
                content = f.readlines()
                for line in content:
                    line = line.strip()
                    if line.startswith(b'nameserver'):
                        parts = line.split()
                        if len(parts) >= 2:
                            server = parts[1]
                            if common.is_ip(server) == socket.AF_INET:
                                if type(server) != str:
                                    server = server.decode('utf-8')
                                self._servers.append(server)
                    
        except (OSError, IOError) as e:
            pass

        if not self._servers:
            self._servers = ['8.8.8.4', '8.8.8.8']
        logging.debug('resolv_servers: %s', self._servers)

    def _parse_hosts(self):
        etc_path = '/etc/hosts'
        try:
            with open(etc_path, 'rb') as f:
                for line in f.readlines():
                    line = line.strip()
                    parts = line.split()
                    if len(parts) >= 2:
                        ip = parts[0]
                        if common.is_ip(ip):
                            for i in range(1, len(parts)):
                                hostname = parts[i]
                                if hostname:
                                    self._hosts[hostname] = ip
        except IOError:
            pass


    def resolve(self, hostname, callback):
        if type(hostname) != bytes:
            hostname = hostname.encode('utf-8')
        if not hostname:
            callback(None, Exception('empty hostname'))
        elif hostname in self._hosts:
            logging.debug('hit hosts: %s', hostname)
            ip = self._hosts[hostname]
            ip = callback((hostname, ip), None)
        
if __name__ == '__main__':
    dns = DNSResolver()
    print(dns._hosts)
    print(dns._servers)
