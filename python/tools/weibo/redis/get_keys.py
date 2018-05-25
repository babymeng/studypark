#!/usr/bin/env python
#coding:utf-8

threads_count = 2

def get_rds_add():
    return [("rs21591.mars.grid.sina.com.cn", 21591, 1)]

def get_keys(thread_data, rds_cli):
    count = 0
    not_found_count = 0
    while True:
        key = rds_cli.randomkey()
        if key.find("_supply") != -1:
            not_found_count = 0
            print key
            count += 1
            if count >= 30:
                break
        else:
            not_found_count += 1
            if not_found_count >= 10000:
                break

