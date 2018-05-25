#!/usr/bin/env python
#coding:utf-8

def get_rds_add():
    return [("rm21798.mars.grid.sina.com.cn", 21798, 7)]

def exp_keys(thread_data, rds_cli):
    print "exp_keys"
    count = 0
    not_found_count = 0
    while True:
        key = rds_cli.randomkey()
        ttl = rds_cli.ttl(key)
        if ttl > 43200:
            rds_cli.expire(key, ttl - 43200)
            count += 1
            not_found_count = 0
            if count % 1000 == 0:
                print count
        else:
            not_found_count += 1

        if not_found_count >= 1000:
            break

