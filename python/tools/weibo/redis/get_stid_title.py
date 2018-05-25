#!/usr/bin/env python
#coding=utf8

import sys
import zlib
import time
import json
import redis

r = redis.Redis(host="rm21559.mars.grid.sina.com.cn", port=21559, db=0)

def set_key():
    key = "1340552632_0"
    value = "{\"segs\": {\"4233086482943626\": {\"duration\": 15000, \"segmentType\": 0, \"exp\": 1524816327}}}"
    r.set(key,value,2590451)


def get_and_set_key():
    key = "4135593049265850_5_HOT"
    key = "4198961231916363_5_HOT"
    #key = "HOT_TOP"
    #key = r.randomkey()
    #print(r.get(key))
    print(zlib.decompress(r.get(key)))
    value = zlib.decompress(r.get(key))
    segment_list = json.loads(value)
    seg_list = []
    for index in segment_list:
        a = {}
        a["story_id"] = index.get("story_id")
        a["created_ts"] = index.get("created_ts")
        a["segment_id"] = index.get("segment_id")
        seg_list.append(a)
    compress_value = zlib.compress(json.dumps(seg_list))
    print(seg_list)
    r.set("4198961231916363_5_NEW", compress_value)


def get_key():
    key = "2656274875"
    #key = "HOT_TOP"
    key = r.randomkey()
    #print(r.get(key))
    #print(zlib.decompress(r.get(key)))
    value = zlib.decompress(r.get(key))
    segment_list = json.loads(value)
    print("%s %d" % (key, len(segment_list)))
    #for index in segment_list:
    #    print "%s %s %s" % (index.get("story_id"),index.get("segment_id"),index.get("created_ts"))

def del_key():
    key = "dis_seg_list"
    r.delete(key)


def main():
    try:
        get_key()
        #set_key()
        #get_and_set_key()
    except Exception as e:
        print("main error: %s" % str(e))


if __name__ == "__main__":
    main()
