#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import sys
import json
import os

__all__ = ['json_view', 'json_str', 'json_file']

_SPACE = ' ' * 4

def json_view(jdict, level = 1, flag = 0, isvalue=False):
    '''
    format the output of dict or list as a json view.
    param: jdcit <dict> or <list>
    param: level <int>
    return: stdout
    '''
    symbol = len(jdict)
    if isinstance(jdict, dict):
        if isvalue:
            print("{")
        else:
            print(_SPACE * (level - 1), "{")
            
        for key in jdict.keys():
            symbol -= 1
            isvalue = True
            print(_SPACE * level, key+": ", end = '')

            if isinstance(jdict[key], dict) or isinstance(jdict[key], list):
                json_view(jdict[key], level + 1, flag, isvalue)
            else:
                if symbol > 0:
                    print(jdict[key], end = '')
                    print(",")
                else:
                    print(jdict[key])
            
        if level > 1:           
            print(_SPACE * (level - 1), "},")
        else:
            print(_SPACE * (level - 1), "}")
        
    elif isinstance(jdict, list):
        if isvalue:
            print("[")
        else:
            print(_SPACE * (level - 1), "[")
            
        for val in jdict:
            symbol -= 1
  
            if isinstance(val, dict) or isinstance(val, list):
                json_view(val, level + 1, flag)
            else:
                if symbol > 0: 
                    print(_SPACE * level, val, end = '')
                    print(",")
                else:
                    print(_SPACE * level, val)
            
        if level > 1:
            print(_SPACE * (level - 1) , "],")
        else:
            print(_SPACE * (level - 1) , "]")

def json_file():
    try:
        filename = sys.argv[1]
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = json.loads(line)
                    json.json_view(line)
        except IOError as e:
            print("Error param:the file '%s' does not exist." % filename)
    except IndexError:
        print('Error param:please input a json file.')

def json_str(jdict = None, level = 1, flag = 0):
    if not sys.stdin.isatty():
        while True:
            json_str = sys.stdin.readline()
            if "" == json_str:
                break
            json_str = json.loads(json_str)
            json.json_view(json_str)
            print("----------------------------------------------------")
    else:
        if jdict is not None:
            json.json_view(jdict, level, flag)

def patch_json():
    if not hasattr(json, "json_view"):
        json.json_view = json_view
    if not hasattr(json, "json_str"):
        json.json_str = json_str

patch_json()

def test1():
    data1 = {"no": 1,
             "val": {"name": {"first": "keky","last": "meng"},
                     "age": [1,2,3],},
             "school": {"xiaoxue": "Hank", "middle": "Mank", "High": "High"}}

    json.json_view(data1)
    
if __name__ == "__main__":
     json_file()
#    test1()
#    test()
