#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import os
import sys
import time
import logging
import shell

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

def daemon_exec(config):
    if 'daemon' in config:
        if os.name != 'posix':
            raise Exception('daemon mode is only supported on Unix.')
        command = config['daemon']
        if not command:
            command = 'start'
        log_file = config["log-file"].decode()
        pid_file = config['pid-file'].decode()
        log_file = os.path.join('../', log_file)
        pid_file = os.path.join('../', pid_file)
        
        if command == 'start':
            daemon_start(pid_file, log_file)
        elif command == 'stop':
            daemon_stop(pid_file)
        elif command == 'restart':
            daemon_stop(pid_file)
            daemon_start(pid_file, log_file)
        else:
            raise Exception('unsupported daemon command %s' % command)

def write_pid_file(pid_file, pid):
    import fcntl
    import stat

    try:
        print("pid_file:", pid_file)
        fd = os.open(pid_file, os.O_RDWR | os.O_CREAT,
                     stat.S_IRUSR | stat.S_IWUSR)
    except IOError as e:
        print("exception e:", e)
        return -1

    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    flags |= fcntl.FD_CLOEXEC
    r     = fcntl.fcntl(fd, fcntl.F_SETFD, flags)

    try:
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB, 0, 0, os.SEEK_SET)
    except IOError:
        r = os.read(fd, 32)
        if r:
            logging.error("already started at pid %s ." % shell.to_str(r))
        else:
            logging.error("already started.")

    os.ftruncate(fd, 0)
    os.write(fd, shell.to_bytes(str(pid)))
    return 0

#打开文件f，取得f的文件描述符oldfd.
#获取stream（标准输出、标准错误）的文件描述符newfd.
#关闭newfd文件流
#将oldfd文件描述符对应的内容赋值给newfd
#也就是说将logfile里的内容复制给了标准输出/标准错误
def freopen(f, mode, stream):
    oldf = open(f, mode)
    oldfd = oldf.fileno()
    newfd = stream.fileno()
    os.close(newfd)
    os.dup2(oldfd, newfd)
    
    #signal.SIGABORT
    #signal.SIGHUP  # 连接挂断
    #signal.SIGILL  # 非法指令
    #signal.SIGINT  # 连接中断
    #signal.SIGKILL # 终止进程（此信号不能被捕获或忽略）
    #signal.SIGQUIT # 终端退出
    #signal.SIGTERM # 终止
    #signal.SIGALRM  # 超时警告
    #signal.SIGCONT  # 继续执行暂停进程
    #设置信号signal.SIGINT处理的函数为handle_exit
    #设置信号signal.SIGTERM处理的函数为handle_exit

def daemon_start(pid_file, log_file):
    print("daemon_start")
    def handle_exit(signum, _):
        if signum == signal.SIGTERM:
            sys.exit(0)
        sys.exit(1)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    pid = os.fork()

    if pid > 0:
        time.sleep(5)
        sys.exit(0)

    ppid = os.getppid()
    pid  = os.getpid()

    #write pid to file
    if write_pid_file(pid_file, pid) != 0:
        os.kill(ppid, signal.SIGINT)
        sys.exit(1)

    #setsid做三个操作：1. 调用进程成为新会话的首进程，2. 调用进程成为新进程组的组长（组长ID就是调用进程ID），3. 没有控制终端
    #如果调用系统函数setsid的进程是进程组组长的话，将会报错，这也是上面第一步必须要做的原因(pid > 0, sleep)
    os.setsid()
    signal.signal(signal.SIG_IGN, signal.SIGHUP)

    print("started daemon process.")
    os.kill(ppid, signal.SIGTERM)

    #文件流重定向
    sys.stdin.close()
    try:
        freopen(log_file, 'a', sys.stdout)
        freopen(log_file, 'a', sys.stderr)
    except IOError as e:
        print("exception e:", e)
        sys.exit(1)

def daemon_stop(pid_file):
    import errno
    try:
        with open(pid_file) as f:
            buf = f.read()
            if not buf:
                logging.error("not running.")
                return
            pid = shell.to_str(buf)
    except IOError as e:
        print("exception e:", e)
        if e.errno == errno.ENOENT:
            logging.error("not running.")
            return
        sys.exit(1)
    pid = int(pid)
    if pid > 0:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            if e.errno == errno.ESRCH:
                logging.error('not running.')
                return
            print('exception e:', e)
            sys.exit(1)
    else:
        logging.error("pid is not positive: %d", pid)

    for i in range(0, 200):
        try:
            os.kill(pid, 0)
        except OSError as e:
            if e.errno == errno.ESRCH:
                break
        time.sleep(0.05)
    else:
        logging.error("timeout when stopping pid %d", pid)
        sys.exit(1)
    print("stopped")
    os.unlink(pid_file)
        
