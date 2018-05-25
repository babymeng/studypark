#!/usr/bin/env python
#coding:utf-8

import sys
import time
import redis
import threading

threads_count = 10

rds_list = [("rm21798.mars.grid.sina.com.cn", 21798, 8)]

def rand_del(index):
    ip, port, db = rds_list[index]
    print str(ip) + ":" + str(port) + " db:" + str(db)
    rds_cli = redis.Redis(ip, port, db) 
    
    count = 0
    while True:
        key = rds_cli.randomkey()
        #print key
        #if key.find("new_") == -1:
        if key != None:
            #print key
            #value = rds_cli.get(key)
            #print "key" + key + " value" + value
            rds_cli.delete(key)
            count += 1
            if count % 1000 == 0:
                print count

if __name__ == '__main__':
    try:
        threads = []
        for i in range(threads_count):
            print i
            index = i % len(rds_list)
            t = threading.Thread(target = rand_del, args=(index,))
            threads.append(t)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()

        print "all over"
    except Exception, exc:
        print exc
