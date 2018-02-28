#!/usr/bin/env python
import os
import sys
import logging
import getopt
import json
import socket
import common

addr = 'fe80::86e:282:9159:2073'
dbyts = [0] * 8
grps = addr.split(':')

for i, v in enumerate(grps):
    if v:
        dbyts[i] = int(v, 16)
    else:
        for j, w in enumerate(grps[::-1]):
            if w:
                dbyts[7 - j] = int(w, 16)
            else:
                break
        break
    
print(dbyts)

res = ((common.chr(i // 256) + common.chr(i % 256)) for i in dbyts)
sss = list(res)
print('sss:', sss)
e = b''.join(sss)
print(e)


addr  = '127.0.0.1'
s = socket.inet_aton(addr)
print(s)


addr = '0:0:0:0:0:ffff:192.1.56.10'
v4addr = addr[addr.rindex(':') + 1:]
print(v4addr)
v4addr = socket.inet_aton(v4addr)
print(v4addr)
v4addr = map(lambda x: ('%02X' % common.ord(x)), v4addr)
v4addr = list(v4addr)
v4addr.insert(2, ':')
print(v4addr)
newaddr = addr[:addr.rindex(':') + 1] + ''.join(v4addr)
print(newaddr)


