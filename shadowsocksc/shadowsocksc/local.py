#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shell
import daemon

def main():
    #check python
    shell.check_python()

    #get config
    print('get config')
    config = shell.get_config(True)

    #start daemon process
    print('daemon_exec')
    daemon.daemon_exec(config)

    #create tcp/udp socket


if __name__ == '__main__':
    main()
