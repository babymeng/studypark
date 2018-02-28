#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import getopt
import json
import socket
import re
import struct

__all__ = ['compat_ord', 'compat_chr', '_ord', '_chr', 'ord', 'chr',
           'to_str', 'to_bytes']

ADDR_TYPE_IPV4 = 1
ADDR_TYPE_DOMAIN = 3
ADDR_TYPE_IPV6 = 4

def compat_ord(s):
    if type(s) == int:
        return s
    else:
        return _ord(s)

def compat_chr(d):
    if bytes == str:
        return _chr(d)
    else:
        return bytes([d])

_ord = ord
_chr = chr
ord = compat_ord
chr = compat_chr

def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s

def to_bytes(s):
    if bytes != str:
        if type(s) == str:
            return s.encode('utf-8')
    return s

#FE80::86E:282:9159:2073
def inet_hton(family, addr):
    addr = to_str(addr)
    if family == socket.AF_INET:
        return socket.inet_aton(addr)
    elif family == socket.AF_INET6:
        if '.' in addr: #a v4 addr [0:0::0:0:ffff:192.1.56.10]
            v4addr = addr[addr.rindex(':') + 1:]
            v4addr = socket.inet_aton(v4addr)
            v4addr = map(lambda x: ('%02X' % ord(x)), v4addr)
            v4addr.insert(2, ':')
            newaddr = addr[:addr.rindex(':') + 1] + ''.join(v4addr)
            return inet_hton(family, newaddr)
        dbyts = [0] * 8
        grps = addr.split(':')
        for i, v in enumerate(grps):
            if v:
                dbyts[i] = int(v, 16)
            else:
                for j, w in enumerate(grps[:: -1]):
                    if w:
                        dbyts[7 - j] = int(w, 16)
                    else:
                        break
                break
        return b''.join((chr(i // 256) + chr(i % 256)) for i in dbyts)
    else:
        logging.error('unknow family %d', family)
        raise RuntimeError("What family?")

def inet_ntoh(family, ipstr):
    #b'\xfe\x80\x00\x00\x00\x00\x00\x00\x08n\x02\x82\x91Y s'
    if family == socket.AF_INET:
        return to_bytes(socket.inet_ntoa(ipstr))
    elif family == socket.AF_INET6:
        v6addr = ':'.join((('%02X%02X') % (ord(i), ord(j))).lstrip('0')
                          for i, j in zip(ipstr[::2], ipstr[1::2]))
        v6addr = re.sub('::+', '::', v6addr, count=1)
    return to_bytes(v6addr)

def is_ip(addr):
    for family in (socket.AF_INET, socket.AF_INET6):
        try:
            if type(addr) != str:
                addr = addr.decode('utf-8')
            inet_hton(family, addr)
            return family
        except (TypeError, ValueError, OSError, IOError):
            pass
    return False

def patch_socket():
    if not hasattr(socket, 'inet_hton'):
        socket.inet_hton = inet_hton

patch_socket()

def parse_header(data):
    addr_type = ord(data[0])
    dst_addr = None
    dst_port = None
    header_length = 0
    if addr_type == ADDR_TYPE_IPV4:
        if len(data) >= 7:
            dst_addr = socket.inet_ntoa(data[1:5])
            dst_port = struct.unpack('>H', data[5:7])[0]
            header_length = 7
        else:
            logging.warn('header is too short.')
    elif addr_type == ADDR_TYPE_IPV6:
        if len(data) >= 19:
            dst_addr = inet_ntoh(data[1:17])
            dst_port = struct.unpack('>H', data[17:19])[0]
            header_length = 19
        else:
            logging.warn('header is too short.')
    elif addr_type == ADDR_TYPE_DOMAIN:
        if len(data) > 2:
            addrlen = ord(data[1])
            if len(data) >= 2 + addrlen:
                dst_addr = data[2:2 + addrlen]
                dst_port = struct.unpack('>H', data[2 + addrlen:4 + addrlen])[0]
                header_len = 4 + addrlen
            else:
                logging.warn('header is too short')
        else:
            logging.warn('header is too short')
    else:
        logging.warn('unsupported addrtype %d, maybe wrong password or '
                     'encryption method' % addr_type)
    if dst_addr is None:
        return None
    return addr_type, to_bytes(dst_addr), dst_port, header_length

def test_inet_xtox():
    ipstr = b'\xfe\x80\x00\x00\x00\x00\x00\x00\x08n\x02\x82\x91Y s'
    v6 = inet_ntoh(socket.AF_INET6, ipstr)
    print(v6)
    assert v6 == b'FE80::86E:282:9159:2073'
    ipv6 = b'FE80::86E:282:9159:2073'
    b = inet_hton(socket.AF_INET6, ipv6)
    assert inet_ntoh(socket.AF_INET6, b) == ipv6

if __name__ == '__main__':
    test_inet_xtox()
