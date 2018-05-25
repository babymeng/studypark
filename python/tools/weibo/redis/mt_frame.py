#!/usr/bin/env python
#coding:utf-8

import sys
import redis
import threading
import signal

#import get_keys as m
#import del_keys as m
#import exp_keys as m
import monitor as m

threads_count = 137

redis_addr_list = m.get_rds_add()

def process(index):
    ip, port, db = redis_addr_list[index]
    #print str(ip) + ":" + str(port) + " db:" + str(db)
    rds_cli = redis.Redis(ip, port, db)

    m.monitor((index, ip, port, db), rds_cli, False)

    #print "thread exit"

def quit(signum, frame):
    print "signal: " + str(signum)
    sys.exit()

if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)

        threads = []
        for i in range(threads_count):
            #print i
            index = i % len(redis_addr_list)
            t = threading.Thread(target = process, args=(index,))
            threads.append(t)

        for t in threads:
            t.setDaemon(True)
            t.start()

        #for t in threads:
        #    t.join()
        while True:
            pass

        print "normally finish"

    except Exception, exc:
        print exc
