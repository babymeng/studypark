#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import redis
import threading

threads_count = 10

rds_list = [("rs24127.mars.grid.sina.com.cn", 24127, 0),
            ("rs22106.mars.grid.sina.com.cn", 22106, 4)]

def random_key(index):
    ip, port, db = rds_list[index]
    #print(str(ip) + ":" + str(port) + " db:" + str(db))
    rds_cli = redis.StrictRedis(ip, port, db)

    count = 1
    while True:
        key = rds_cli.randomkey()
        key = key.decode()[1:-6]
        
        print(key)
        #print("id_thread:"+ str(id_thread) + " " + key)
        count += 1

        if count > 10010:
            break

if __name__ == '__main__':
    try:
        threads = []
        for i in range(threads_count):
            index = 1
            #print("index=", index)
            t = threading.Thread(target=random_key, args=(index,))
            threads.append(t)
        #print("--------1--------")
        for t in threads:
            t.setDaemon(True)
            t.start()
        #print("--------2--------")
        for t in threads:
            t.join()
        #print("--------3--------")
    except Exception as e:
        #print(str(e))
        pass
    
