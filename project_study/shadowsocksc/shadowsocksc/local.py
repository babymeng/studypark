#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shell
import daemon
import tcprelay
import eventloop
import logging
import signal

def main():
    #check python
    shell.check_python()

    #get config
    print('get config')
    config = shell.get_config(True)

    #start daemon process
    print('daemon_exec')
    daemon.daemon_exec(config)

    logging.info("starting local at %s:%d" %
                     (config['local_address'], config['local_port']))
    #create tcp/udp socket
    tcp_server = tcprelay.TCPRelay(config, None, True)
    loop = eventloop.EventLoop()
    tcp_server.add_to_loop(loop)

    def handler(signum, _):
        logging.warn('received SIGQUIT, doing graceful shutting down...')
        tcp_server.close(next_tick=True)

    signal.signal(getattr(signal, 'SIGQUIT', signal.SIGTERM), handler)

    def int_handler(signum, _):
        sys.exit(1)
    signal.signal(signal.SIGINT, int_handler)

    loop.run()

if __name__ == '__main__':
    main()
