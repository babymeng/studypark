#!/usr/bin/env python

import redis
import sys
import os
import zlib
import json
import kekys

_redis_host = []
_fail_host = []
_key = "4232789609803330_info"


def get_host(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            _redis_host.append(line)

def connect():
    for host in _redis_host:
        try:
            r = redis.StrictRedis(host=host, port=6379, db=1)
            value = (zlib.decompress(r.get(_key)))
            v1 = json.loads(value)
            print(host + ": " + str(v1["url_objects"][0]["play_count"]))
        except Exception as e:
            _fail_host.append(host)
            print(host + ": err" )
    for host in _fail_host:
        try:
            r = redis.StrictRedis(host=host, port=6379, db=1)
            value = (zlib.decompress(r.get(_key)))
            v1 = json.loads(value)
            print(host + ": " + str(v1["url_objects"][0]["play_count"]))
        except Exception as e:
            print(host + ": nil" )

def main():
    get_host("ip_list")
    connect()

if __name__ == "__main__":
    main()

    
