#!/usr/bin/env python
#coding:utf-8

import sys
import redis
import time
import json
import hashlib
import urllib2
import socket
import urllib
import random

import openAPI

def get_segment_info(seg_id):
    result = ""
    try:
        uid = "2232130087"
        url = "http://i.api.weibo.com/2/stories/get_segments.json?source=4050779375&segment_ids=" + seg_id
        result = openAPI.read_url_by_GET_with_Tauth(url, uid)

    except Exception, e:
        print "get_segment_info error: %s" % str(e)

    return result


def main(sgid_file):
    try:
        with open(sgid_file) as fp:
            for line in fp:
                line_str = line.strip()
                result = get_segment_info(line_str)
                print "%s" % (result)
                time.sleep(0.1)
                break

    except Exception, e:
        print "main error: %s" % str(e)


if __name__ == "__main__":
    main(sys.argv[1])
