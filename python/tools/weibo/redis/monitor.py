#!/usr/bin/env python
#coding:utf-8

import time

threads_count = 1

def get_rds_add():

    return [("rc20161.mars.grid.sina.com.cn", 20161, 0),
            ("rc20162.mars.grid.sina.com.cn", 20162, 0),
            ("rc20163.mars.grid.sina.com.cn", 20163, 0),
            ("rc21464.eos.grid.sina.com.cn", 21464, 0),
            ("rc6981.mars.grid.sina.com.cn", 6981, 0),
            ("rc6982.mars.grid.sina.com.cn", 6982, 0),
            ("rc7608.eos.grid.sina.com.cn", 7608, 0),
            ("rc7608.hebe.grid.sina.com.cn", 7608, 0),
            ("rc7609.eos.grid.sina.com.cn", 7609, 0),
            ("rc7609.hebe.grid.sina.com.cn", 7609, 0),
            ("rc7618.eos.grid.sina.com.cn", 7618, 0),
            ("rc7618.hebe.grid.sina.com.cn", 7618, 0),
            ("rc7619.eos.grid.sina.com.cn", 7619, 0),
            ("rc7619.hebe.grid.sina.com.cn", 7619, 0),
            ("rm11108.eos.grid.sina.com.cn", 11108, 0),
            ("rm11333.eos.grid.sina.com.cn", 11333, 0),
            ("rm20042.eos.grid.sina.com.cn", 20042, 0),
            ("rm20093.eos.grid.sina.com.cn", 20093, 0),
            ("rm20370.eos.grid.sina.com.cn", 20370, 0),
            ("rm20371.eos.grid.sina.com.cn", 20371, 0),
            ("rm20372.eos.grid.sina.com.cn", 20372, 0),
            ("rm20396.eos.grid.sina.com.cn", 20396, 0),
            ("rm21062.mars.grid.sina.com.cn", 21062, 0),
            ("rm21352.eos.grid.sina.com.cn", 21352, 0),
            ("rm21353.eos.grid.sina.com.cn", 21353, 0),
            ("rm21559.mars.grid.sina.com.cn", 21559, 0),
            ("rm21560.mars.grid.sina.com.cn", 21560, 0),
            ("rm21561.mars.grid.sina.com.cn", 21561, 0),
            ("rm21562.mars.grid.sina.com.cn", 21562, 0),
            ("rm21564.mars.grid.sina.com.cn", 21564, 0),
            ("rm21565.mars.grid.sina.com.cn", 21565, 0),
            ("rm21566.mars.grid.sina.com.cn", 21566, 0),
            ("rm21567.mars.grid.sina.com.cn", 21567, 0),
            ("rm21581.mars.grid.sina.com.cn", 21581, 0),
            ("rm21590.mars.grid.sina.com.cn", 21590, 0),
            ("rm21591.mars.grid.sina.com.cn", 21591, 0),
            ("rm21592.mars.grid.sina.com.cn", 21592, 0),
            ("rm21593.mars.grid.sina.com.cn", 21593, 0),
            ("rm21594.mars.grid.sina.com.cn", 21594, 0),
            ("rm21736.mars.grid.sina.com.cn", 21736, 0),
            ("rm21737.mars.grid.sina.com.cn", 21737, 0),
            ("rm21749.mars.grid.sina.com.cn", 21749, 0),
            ("rm21777.mars.grid.sina.com.cn", 21777, 0),
            ("rm21781.mars.grid.sina.com.cn", 21781, 0),
            ("rm21782.mars.grid.sina.com.cn", 21782, 0),
            ("rm21798.mars.grid.sina.com.cn", 21798, 0),
            ("rm21937.mars.grid.sina.com.cn", 21937, 0),
            ("rm21938.mars.grid.sina.com.cn", 21938, 0),
            ("rm21996.mars.grid.sina.com.cn", 21996, 0),
            ("rm22003.mars.grid.sina.com.cn", 22003, 0),
            ("rm22017.mars.grid.sina.com.cn", 22017, 0),
            ("rm22018.mars.grid.sina.com.cn", 22018, 0),
            ("rm22019.mars.grid.sina.com.cn", 22019, 0),
            ("rm22049.mars.grid.sina.com.cn", 22049, 0),
            ("rm22106.mars.grid.sina.com.cn", 22106, 0),
            ("rm22171.mars.grid.sina.com.cn", 22171, 0),
            ("rm22330.mars.grid.sina.com.cn", 22330, 0),
            ("rm22484.mars.grid.sina.com.cn", 22484, 0),
            ("rm23100.mars.grid.sina.com.cn", 23100, 0),
            ("rm23154.mars.grid.sina.com.cn", 23154, 0),
            ("rm7109.eos.grid.sina.com.cn", 7109, 0),
            ("rm7114.eos.grid.sina.com.cn", 7114, 0),
            ("rm7122.mars.grid.sina.com.cn", 7122, 0),
            ("rm7124.mars.grid.sina.com.cn", 7124, 0),
            ("rm7138.eos.grid.sina.com.cn", 7138, 0),
            ("rm7139.mars.grid.sina.com.cn", 7139, 0),
            ("rm7183.eos.grid.sina.com.cn", 7183, 0),
            ("rm7186.eos.grid.sina.com.cn", 7186, 0),
            ("rm7365.eos.grid.sina.com.cn", 7365, 0),
            ("rm7388.eos.grid.sina.com.cn", 7388, 0),
            ("rm7416.eos.grid.sina.com.cn", 7416, 0),
            ("rm8895.eos.grid.sina.com.cn", 8895, 0),
            ("rm8896.eos.grid.sina.com.cn", 8896, 0),
            ("rm8898.eos.grid.sina.com.cn", 8898, 0),
            ("rm8899.eos.grid.sina.com.cn", 8899, 0),
            ("rm8900.eos.grid.sina.com.cn", 8900, 0),
            ("rs11108.atlas.grid.sina.com.cn", 11108, 0),
            ("rs11108.hebe.grid.sina.com.cn", 11108, 0),
            ("rs11333.hebe.grid.sina.com.cn", 11333, 0),
            ("rs20042.mars.grid.sina.com.cn", 20042, 0),
            ("rs20093.hebe.grid.sina.com.cn", 20093, 0),
            ("rs20370.hebe.grid.sina.com.cn", 20370, 0),
            ("rs20371.hebe.grid.sina.com.cn", 20371, 0),
            ("rs20372.hebe.grid.sina.com.cn", 20372, 0),
            ("rs20396.hebe.grid.sina.com.cn", 20396, 0),
            ("rs20605.hebe.grid.sina.com.cn", 20605, 0),
            ("rs21062.mars.grid.sina.com.cn", 21062, 0),
            ("rs21352.mars.grid.sina.com.cn", 21352, 0),
            ("rs21353.mars.grid.sina.com.cn", 21353, 0),
            ("rs21559.mars.grid.sina.com.cn", 21559, 0),
            ("rs21560.mars.grid.sina.com.cn", 21560, 0),
            ("rs21561.mars.grid.sina.com.cn", 21561, 0),
            ("rs21562.mars.grid.sina.com.cn", 21562, 0),
            ("rs21581.mars.grid.sina.com.cn", 21581, 0),
            ("rs21590.mars.grid.sina.com.cn", 21590, 0),
            ("rs21591.mars.grid.sina.com.cn", 21591, 0),
            ("rs21592.mars.grid.sina.com.cn", 21592, 0),
            ("rs21593.mars.grid.sina.com.cn", 21593, 0),
            ("rs21594.mars.grid.sina.com.cn", 21594, 0),
            ("rs21736.mars.grid.sina.com.cn", 21736, 0),
            ("rs21737.mars.grid.sina.com.cn", 21737, 0),
            ("rs21749.mars.grid.sina.com.cn", 21749, 0),
            ("rs21777.mars.grid.sina.com.cn", 21777, 0),
            ("rs21781.mars.grid.sina.com.cn", 21781, 0),
            ("rs21782.mars.grid.sina.com.cn", 21782, 0),
            ("rs21798.mars.grid.sina.com.cn", 21798, 0),
            ("rs21937.mars.grid.sina.com.cn", 21937, 0),
            ("rs21938.mars.grid.sina.com.cn", 21938, 0),
            ("rs21996.mars.grid.sina.com.cn", 21996, 0),
            ("rs22003.mars.grid.sina.com.cn", 22003, 0),
            ("rs22017.mars.grid.sina.com.cn", 22017, 0),
            ("rs22049.mars.grid.sina.com.cn", 22049, 0),
            ("rs22106.mars.grid.sina.com.cn", 22106, 0),
            ("rs22330.mars.grid.sina.com.cn", 22330, 0),
            ("rs22484.mars.grid.sina.com.cn", 22484, 0),
            ("rs23100.mars.grid.sina.com.cn", 23100, 0),
            ("rs23154.mars.grid.sina.com.cn", 23154, 0),
            ("rs7109.hebe.grid.sina.com.cn", 7109, 0),
            ("rs7114.hebe.grid.sina.com.cn", 7114, 0),
            ("rs7118.eos.grid.sina.com.cn", 7118, 0),
            ("rs7118.mars.grid.sina.com.cn", 7118, 0),
            ("rs7122.eos.grid.sina.com.cn", 7122, 0),
            ("rs7124.eos.grid.sina.com.cn", 7124, 0),
            ("rs7138.eos.grid.sina.com.cn", 7138, 0),
            ("rs7138.hebe.grid.sina.com.cn", 7138, 0),
            ("rs7183.hebe.grid.sina.com.cn", 7183, 0),
            ("rs7184.eos.grid.sina.com.cn", 7184, 0),
            ("rs7184.hebe.grid.sina.com.cn", 7184, 0),
            ("rs7186.eos.grid.sina.com.cn", 7186, 0),
            ("rs7186.hebe.grid.sina.com.cn", 7186, 0),
            ("rs7365.hebe.grid.sina.com.cn", 7365, 0),
            ("rs7388.hebe.grid.sina.com.cn", 7388, 0),
            ("rs7416.hebe.grid.sina.com.cn", 7416, 0),
            ("rs8896.mars.grid.sina.com.cn", 8896, 0),
            ("rs8898.mars.grid.sina.com.cn", 8898, 0),
            ("rs8899.mars.grid.sina.com.cn", 8899, 0),
            ("rs8900.mars.grid.sina.com.cn", 8900, 0)]

    #return [("10.85.132.235", 6789, 0)]

def hit_rate(rds_info_json, last_keyspace_hits, last_keyspace_misses):
    if rds_info_json != None                        \
        and rds_info_json["keyspace_hits"] != None  \
        and rds_info_json["keyspace_misses"] != None:
        keyspace_hits = rds_info_json["keyspace_hits"]
        keyspace_misses = rds_info_json["keyspace_misses"]

        print (keyspace_hits - last_keyspace_hits + 0.0)     \
            / ((keyspace_hits - last_keyspace_hits) + (keyspace_misses - last_keyspace_misses))

        return (keyspace_hits, keyspace_misses)

def miss(rds_info_json, last_keyspace_misses):
    if rds_info_json != None                        \
        and rds_info_json["keyspace_misses"] != None:
        keyspace_misses = rds_info_json["keyspace_misses"]

        print keyspace_misses - last_keyspace_misses

        return keyspace_misses

def space(thread_data, rds_info_json, conf_json):
    maxmemory = int(conf_json["maxmemory"])
    used_memory = float(rds_info_json["used_memory"])
    if maxmemory != 0:
        ratio = used_memory / maxmemory
        if ratio > 0.8:
            maxmemory_policy = conf_json["maxmemory-policy"]
            space_info = str(thread_data) + " " + maxmemory_policy + " " + str(ratio)
            print space_info

def monitor(thread_data, rds_cli, loop):
    last_keyspace_hits, last_keyspace_misses = 0, 0
    while True:
        rds_info_json = rds_cli.info()
        conf_json = rds_cli.config_get("*")
        #miss(rds_info_json, last_keyspace_misses)
        #last_keyspace_hits, last_keyspace_misses = hit_rate(rds_info_json, last_keyspace_hits, last_keyspace_misses)
        space(thread_data, rds_info_json, conf_json)
        #time.sleep(1)

        if not loop:
            break

