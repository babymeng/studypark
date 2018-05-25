#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pickle;

pikcle_file = []

def pickle_save(file):
    f1 = open('./temp.pkl', 'wb')
    try:
        with open(file, "rb") as f:
            p1 = pickle.dump(f, f1, True)
    except IOError as err:
        print("File Error" + str(err))
        f1.close()  
    except pickle.PickleError as perr:
        print("Pickle Error" + str(perr))
        f1.close()
    f1.close()  

def pickle_load(file):
    try:
        with open(file, "wb") as f:
            pickle.load(f)
    except IOError as err:
        print("File Error" + str(err))
    except pickle.PickleError as perr:
        print("Pickle Error" + str(perr))

if __name__ == '__main__':
    pickle_save("/Users/xiangqian5/Music/my/yatou.txt")
    #pickle_load("/Users/xiangqian5/Movies/mov.mov")
