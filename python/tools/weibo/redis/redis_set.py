#!/usr/bin/env python
#coding=utf8

import sys
import zlib
import time
import json
import redis

#r = redis.Redis(host="rm22106.mars.grid.sina.com.cn", port=22106, db=3)
#r = redis.Redis(host="rs24156.mars.grid.sina.com.cn", port=24156, db=2)
#r = redis.Redis(host="rm22195.mars.grid.sina.com.cn", port=22195, db=2)
r = redis.Redis(host="10.85.132.235", port=4133, db=3)

def set_key():
    key = "4135593049265850_5"
    value = zlib.decompress(r.get(key))
    segment_list = json.loads(value)
    time_now = int(time.time())
    time_span = time_now - 36000
    seg_list = []
    stid_list = ["5897589628_0","2669151847_0","5200791004_0","1763552305_0","5201562343_0","3686807071_0","5878832944_0","1639335284_0","1905262027_0","1905262027_0","1905262027_0"]
    sgid_list = ["4184463854584234","4184470687372174","4184471337274455","4184223068261796","4184472239195558","4184525762331412","4184547409737843","4184524621473911","4184467356947176","4184474264841343","4184474760016505"]

    for index in range(0,11):
        a = {}
        a["story_id"] = stid_list[index]
        a["segment_id"] = sgid_list[index]
        a["created_ts"] = time_now
        seg_list.append(a)

    for index in segment_list:
        if index.get("created_ts") > time_span:
            a = {}
            a["story_id"] = index.get("story_id")
            a["created_ts"] = index.get("created_ts")
            a["segment_id"] = index.get("segment_id")
            seg_list.append(a)

    new_key = "dis_seg_list"
    compress_value = zlib.compress(json.dumps(seg_list))
    r.set(new_key, compress_value)


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
    print "%s %s" % (key, value)
    #for index in segment_list:
    #    print "%s %s %s" % (index.get("story_id"),index.get("segment_id"),index.get("created_ts"))

def del_key():
    key = "dis_seg_list"
    r.delete(key)


def main():
    try:
        #set_key()
        #get_and_set_key()
        get_key()
    except Exception, e:
        print "main error: %s" % str(e)


if __name__ == "__main__":
    main()
