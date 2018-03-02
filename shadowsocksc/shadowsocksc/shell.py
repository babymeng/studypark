#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import getopt
import json

VERBOSE_LEVEL = 5

verbose = 0

def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s

def to_bytes(s):
    if bytes != str:
        if type(s) == str:
            return s.encode('utf-8')
    return s

def check_python():
    info = sys.version_info
    logging.debug("info:%s", info)

    if info[0] == 2 and not info[1] >=6:
        logging.debug("python 2.6+ required")
        sys.exit(1)
    elif info[0] == 3 and not info[1] >= 3:
        logging.debug("python 3.3+ required")
        sys.exit(1)
    elif info[0] not in [2, 3]:
        logging.debug("python version not supported")
        sys.exit(1)

def find_config():
    config_path = 'config.json'
    if os.path.exists(config_path):
        return config_path
    config_path = os.path.join(os.path.dirname(__file__), '../', 'config.json')
    if os.path.exists(config_path):
        return config_path
    return None

def get_config(is_local):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(lineno)-4d %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    if is_local:
        shortopts = "hd:s:b:p:k:l:m:c:t:vq"
        longopts  = ['help', 'fast-open', 'pid-file=', 'log-file=', 'user=', 'version']
    else:
        shortopts = 'hd:s:p:k:m:c:t:vq'
        longopts  = ['help', 'fast-open', 'pid-file=', 'log-file=', 'user=', 'workers=', 'forbidden-ip=', 'manager-address=', 'version']
    config_path = find_config()

    optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
    for key, value in optlist:
        if key == '-c':
            config_path = value

    logging.info("config_path:%s", config_path)
    print("config_path", config_path)
    if config_path:
        logging.info("loading config from %s" % config_path)
        with open(config_path, 'r') as f:
            try:
                config = _parse_json_in_str(f.read())
            except ValueError as e:
                logging.error('found an error in config.json: %s' % e.message)
                print('found an error in config.json:', e.message)
                sys.exit(1)
    else:
        config = {}

    logging.info("config:%s" % config)
    print('config:', config)

    v_count = 0
    print("optlist:", optlist)
    for key, value in optlist:
        if key == '-p':
            config['server-port'] = int(value)
        elif key == '-k':
            config['password'] = to_bytes(value)
        elif key == '-l':
            config['local_port'] = int(value)
        elif key == '-s':
            config['server'] = to_str(value)
        elif key == '-m':
            config['methon'] = to_str(value)
        elif key == '-b':
            config['local_address'] = to_string(value)
        elif key == '-v':
            v_count += 1
            config['verbose'] = v_count
        elif key == '-t':
            config['timeout'] = int(value)
        elif key == '-d':
            config['daemon'] = to_str(value)
            print('daemon', value)
        elif key in ('-h', '--help'):
            if is_local:
                print_local_help()
            else:
                print_server_help()
            sys.exit(0)
        elif key == '--log-file':
            config['log-file'] = to_str(value)
        elif key == '--pid-file':
            config['pid-file'] = to_str(value)
        elif key == '-q':
            v_count -= 1
            config['verbose'] = v_count

    if not config:
        logging.error('config not specified')
        print_help(is_local)
        sys.exit(2)
            
    config['password'] = to_bytes(config.get('password', b''))
    config['method'] = to_str(config.get('method', 'rc4-md5'))
    config['port_password'] = config.get('port_password', None)
    config['timeout'] = int(config.get('timeout', 60))
    config['fast_open'] = config.get('fast_open', False)
    #config['workers'] = config.get('workers', 1)
    config['pid-file'] = config.get('pid-file', '../shadowsocks.pid')
    config['log-file'] = config.get('log-file', '../shadowsocks.log')
    config['verbose'] = config.get('verbose', False)
    config['local_address'] = to_str(config.get('local_address', '127.0.0.1'))
    config['local_port'] = config.get('local_port', 1080)
    if is_local:
        if config.get('server', None) is None:
            logging.error('server addr not specified')
            print_local_help()
            sys.exit(2)
        else:
            config['server'] = to_str(config['server'])
    else:
        config['server'] = to_str(config.get('server', '0.0.0.0'))
    config['server_port'] = config.get('server_port', 8388)

    logging.info("config$: %s" % config)
    print("config$", config)
        
    return config

def print_help(is_local):
    if is_local:
        print_local_help()
    else:
        print_server_help()


def print_local_help():
    print('''usage: sslocal [OPTION]...
A fast tunnel proxy that helps you bypass firewalls.

You can supply configurations via either config file or command line arguments.

Proxy options:
  -c CONFIG              path to config file
  -s SERVER_ADDR         server address
  -p SERVER_PORT         server port, default: 8388
  -b LOCAL_ADDR          local binding address, default: 127.0.0.1
  -l LOCAL_PORT          local port, default: 1080
  -k PASSWORD            password
  -m METHOD              encryption method, default: aes-256-cfb
  -t TIMEOUT             timeout in seconds, default: 300
  --fast-open            use TCP_FASTOPEN, requires Linux 3.7+

General options:
  -h, --help             show this help message and exit
  -d start/stop/restart  daemon mode
  --pid-file PID_FILE    pid file for daemon mode
  --log-file LOG_FILE    log file for daemon mode
  --user USER            username to run as
  -v, -vv                verbose mode
  -q, -qq                quiet mode, only show warnings/errors
  --version              show version information

Online help: <https://github.com/shadowsocks/shadowsocks>
''')


def print_server_help():
    print('''usage: ssserver [OPTION]...
A fast tunnel proxy that helps you bypass firewalls.

You can supply configurations via either config file or command line arguments.

Proxy options:
  -c CONFIG              path to config file
  -s SERVER_ADDR         server address, default: 0.0.0.0
  -p SERVER_PORT         server port, default: 8388
  -k PASSWORD            password
  -m METHOD              encryption method, default: aes-256-cfb
  -t TIMEOUT             timeout in seconds, default: 300
  --fast-open            use TCP_FASTOPEN, requires Linux 3.7+
  --workers WORKERS      number of workers, available on Unix/Linux
  --forbidden-ip IPLIST  comma seperated IP list forbidden to connect
  --manager-address ADDR optional server manager UDP address, see wiki

General options:
  -h, --help             show this help message and exit
  -d start/stop/restart  daemon mode
  --pid-file PID_FILE    pid file for daemon mode
  --log-file LOG_FILE    log file for daemon mode
  --user USER            username to run as
  -v, -vv                verbose mode
  -q, -qq                quiet mode, only show warnings/errors
  --version              show version information

Online help: <https://github.com/shadowsocks/shadowsocks>
''')

def _decode_list(data):
    rv = []
    for item in data:
        if hasattr(item, 'encode'):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.items():
        if hasattr(value, 'encode'):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def _parse_json_in_str(data):
    return json.loads(data, object_hook=_decode_dict)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(lineno)-4d %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    check_python()
    get_config(True)
