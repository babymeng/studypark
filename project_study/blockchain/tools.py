#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('64s', ifname[:15])
    )[20:24])


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    fcntl.ioctl(s.fileno(), 0x8915, struct.pack('64s', 'eth0'))
