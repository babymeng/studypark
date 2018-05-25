#!/usr/bin/env python
#coding:utf-8

import sys
import redis
import time
import json
import hashlib

import socket
import urllib
import random

import openAPI

def get_weibo_info(mid):
    result = ""
    try:
        uid = "2232130087"
        url = "http://i.api.weibo.com/2/statuses/show_batch.json?source=981203697&trim_user=1&ids=" + mid
        result = openAPI.read_url_by_GET_with_Tauth(url, uid)

    except Exception as e:
        print("get_segment_info error: %s" % str(e))

    return result


def read_mid_file(mid_file):
    try:
        with open(mid_file) as fp:
            for line in fp:
                line_str = line.strip()
                result = get_weibo_info(line_str)
                print("%s" % (result))
                time.sleep(0.1)
                break

    except Exception as e:
        print("main error: %s" % str(e))

def read_mid_list(mid_str_list):
    if '[' == mid_str_list[0]:
        mid_str_list = mid_str_list[1:-1]
    mid_list = mid_str_list.split(",")
    for mid in mid_list:
        result = get_weibo_info(mid)
        if type(result) == bytes:
            result = result.decode('utf-8')
        print("%s" % (result))
        time.sleep(0.1)

if __name__ == "__main__":
    #read_mid_file(sys.argv[1])
    read_mid_list(sys.argv[1])
