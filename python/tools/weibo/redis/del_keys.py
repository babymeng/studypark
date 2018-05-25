#!/usr/bin/env python
#coding:utf-8

import sys
sys.path.append("..")
import time
import common.sendmail as sm

limit_key_count = 20000000
del_once = 200000
addr_list = ["yingchun5@staff.weibo.com"]

def get_rds_add():
    return [("rm21798.mars.grid.sina.com.cn", 21798, 7)]

def get_key_count(rds_cli, db):
    key_count = 0
    rds_info_json = rds_cli.info()
    if rds_info_json != None                    \
        and rds_info_json[db] != None           \
        and rds_info_json[db]["keys"] != None:
        key_count = rds_info_json[db]["keys"]
    return key_count

def del_keys(thread_data, rds_cli):
    while True:
        db7_key_count = get_key_count(rds_cli, "db7")

        msg = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " db7 keys:" + str(db7_key_count)
        print msg

        recover = False
        while db7_key_count > limit_key_count:
            if thread_data == 0:
                sm.send_mail(addr_list, "21798 alert", msg)

            count = 0
            while count < del_once:
                key = rds_cli.randomkey()
                if key != None:
                    rds_cli.delete(key)
                    count += 1
                    if count % 5000 == 0:
                        print count

            db7_key_count = get_key_count(rds_cli, "db7")
            if db7_key_count <= limit_key_count:
                recover = True

        if recover:
            msg = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " db7 keys:" + str(db7_key_count)
            if thread_data == 0:
                sm.send_mail(addr_list, "21798 alert recover", msg)
            print msg

        time.sleep(60)

