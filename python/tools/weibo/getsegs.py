#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import getopt
import sys
import json
import kekys
import os

'''
算法：story_id第3位和第4位，对4取模，找到对应redis
0 rs21559.mars.grid.sina.com.cn:21559
1 rs21560.mars.grid.sina.com.cn:21560
2 rs21561.mars.grid.sina.com.cn:21561
3 rs21562.mars.grid.sina.com.cn:21562
'''

_REDIS_DB = ["rs21559.mars.grid.sina.com.cn:21559",
             "rs21560.mars.grid.sina.com.cn:21560",
             "rs21561.mars.grid.sina.com.cn:21561",
             "rs21562.mars.grid.sina.com.cn:21562"]

_REDIS = [{"host": "rs21559.mars.grid.sina.com.cn", "port": 21559},
          {"host": "rs21560.mars.grid.sina.com.cn", "port": 21560},
          {"host": "rs21561.mars.grid.sina.com.cn", "port": 21561},
          {"host": "rs21562.mars.grid.sina.com.cn", "port": 21562}]

_LOG_DIR = os.getcwd() + '/segs/'

def write_to_file(segs, filename):
    try:
        os.mkdir(_LOG_DIR)
    except FileExistsError:
        pass
    
    try:
        with open(filename, 'w') as f:
           json.dump(segs, f)
    except FileNotFoundError:
        print("file not exist.")

def get_redis(stid):
    stid_3rd_4th = str.strip(stid[2:4])
    index = int(stid_3rd_4th) % 4
    redis_db = _REDIS[index]

    return redis_db["host"], redis_db["port"]

def get_segs_by_stid(stid):
    host, port = get_redis(stid)
    
    redis_client = redis.StrictRedis(host=host, port=port, db=0)
    segs = redis_client.get(stid)
    try:
        segs = json.loads(segs.decode())
        json.json_str(segs)
    except AttributeError:
        print("no such segments for the storyid:", stid)
        exit(0)

    return segs

def main():
    stid = sys.argv[1]
    segs = get_segs_by_stid(stid)

    filename = _LOG_DIR + "segs_" + stid + ".json"
    print(filename)
    write_to_file(segs, filename)

if __name__ == '__main__':
    main()
