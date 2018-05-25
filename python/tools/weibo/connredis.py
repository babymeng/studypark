#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import getopt
import sys
import json
import kekys
import os
import zlib

_REDIS_S = [
            {"host": "rs23473.mars.grid.sina.com.cn", "port": 23473, "db": 1},
            {"host": "127.0.0.1", "port": 6379, "db": 0}
            ]

_REDIS_M = [
            {"host": "rm23473.mars.grid.sina.com.cn", "port": 23473, "db": 1},
            ]

IDENTIFY_MAIN  = 1
IDENTIFY_SLAVE = 0

def get_redis(identify=IDENTIFY_SLAVE, index=0):
    if identify == IDENTIFY_SLAVE:
        redis_db = _REDIS_S[index]
    elif identify == IDENTIFY_MAIN:
        redis_db = _REDIS_M[index]
        
    return redis_db["host"], redis_db["port"], redis_db["db"]

def connect_redis(identify=IDENTIFY_SLAVE, index=0):
    try:
        host, port, db = get_redis(index=index)
        cli_redis = redis.StrictRedis(host=host, port=port, db=db)
    except Exception as e:
        host, port, db = get_redis(IDENTIFY_MAIN, index)
        cli_redis = redis.StrictRedis(host=host, port=port, db=db)

    return cli_redis

def get_value():
    pass

def set_key(r):
    key = "4135593049265850_5"
    stid_list = ["5897589628_0","2669151847_0","5200791004_0","1763552305_0","5201562343_0","3686807071_0","5878832944_0","1639335284_0","1905262027_0","1905262027_0","1905262027_0"]
    print(stid_list)    
    j_v = json.dumps(stid_list)
    print("j_v", j_v)
    z_v = zlib.compress(j_v.encode())
    print("z_v", z_v)
    r.set(key, z_v)

def random_key(r):
    key = r.randomkey()
    value = r.get(key)
    print(key)
    print(value)

def main(r):
    try:
        random_key(r)
        set_key(r)
    except Exception as e:
        print("main error: %s" % str(e))

if __name__ == "__main__":
    r = connect_redis(index=1)
    main(r)
    
