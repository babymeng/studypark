#!/usr/bin/env python
#coding=utf8

import sys
import zlib
import redis

key = sys.argv[1]

#r = redis.Redis(host="rs22106.mars.grid.sina.com.cn", port=22106, db=3)
#r = redis.Redis(host="rs21737.mars.grid.sina.com.cn", port=21737, db=1)
#r = redis.Redis(host="rm21798.mars.grid.sina.com.cn", port=21798, db=1)
#r = redis.Redis(host="rs23100.mars.grid.sina.com.cn", port=23100, db=1)
r = redis.Redis(host="rs21592.mars.grid.sina.com.cn", port=21592, db=4)

if key == "r":
    key = r.randomkey()
compress_value = r.get(key)
#compress_value = zlib.compress("hello world")
if compress_value != None:
    print(zlib.decompress(compress_value))
else:
    print compress_value
