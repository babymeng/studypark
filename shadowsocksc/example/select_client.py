#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import socket
import time

def select_client():
    server_addrs = ('127.0.0.1', 1083)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_addrs)
    time.sleep(1)
    
    msg = b"Hello:I'm client!"
    client.send(msg)
    
    time.sleep(1)
    client.send(b'\n\n')
    client.close()
                
if __name__ == '__main__':
    select_client()
