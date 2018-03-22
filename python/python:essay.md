# Python 随笔

#### os.path.exists判断文件是否存在  
```python
>>> import os
>>> import sys
>>> os.path.exists('setup.py')
True
>>> 
```

#### os.path.dirname(\_\_file\_\_)获取python文件运行时的路径
###### (在idle中运行会报错，因为没有从文件中运行)
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

print(os.path.dirname(__file__))
print(os.path.dirname('/Users/helen/Workspace/code/shadowsocks/mytest/mytest.py'))
print(os.path.dirname('shadowsocks/mytest/mytest.py'))

result:
/Users/xiangqian5/OpenSourceSoft/shadowsocks
/Users/helen/Workspace/code/shadowsocks/mytest
shadowsocks/mytest

```

#### getopt.getopt(sys.argv[1:], shortopts, longopts)获取命令行参数
* 参数sys.argv[1:]从命令行的第二个参数开始进行接收（第一个参数是脚本名）   
* 参数shortopts:短参数.个人理解就是单个字母'h'之类的。本文中shortopts = 'hd:s:b:p:k:l:m:c:t:vq' 字母后没有‘:’的，表示后边不带参数，带':'表示后边有参数    
* 参数longopts:长参数.即匹配的option是单个单词，option后有‘=’的带有有参数，不带的没有参数.长参数的option:  --help  --longfile file.log
* 返回值：option的list，和参数的list

```python
eg:  python mytest.py -h -u root

shortopts = 'hd:s:b:p:k:l:m:c:t:vq'
longopts = ['help', 'fast-open', 'pid-file=', 'log-file=', 'user=']
optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
[('-h', ''), ('-u', 'root')] []
optlist = [('-h', ''), ('-u', 'root')] 
args = []
```

#### dict


##### dict.get('key1', 'defaultvalue') 
###### 从字典中获取键为key1的value，如果指定的键不存在时，返回默认值‘defaultvalue’
```python
>>> 
>>> person = {'name': 'Lily', 'sex': 'w'}
>>> person.get('name')
'Lily'
>>> person.get('age')
>>> person.get('age', 20)
20
>>> 
```

##### dict = collections.defaultdict(factory_func)
###### defaultdict属于内建函数dict的一个子类，调用工厂函数factory_func提供缺失的key对应的 value值.dict[item] = value,当item不存在时会创建对应条目并赋值为value.
```python
>>> import collections
>>> str = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
>>> dd = collections.defaultdict(list)
>>> for k, v in str:
        dd[k].append(v)
    
>>> dd
defaultdict(<class 'list'>, {'yellow': [1, 3], 'blue': [2, 4], 'red': [1]})
>>> dd.items()
dict_items([('yellow', [1, 3]), ('blue', [2, 4]), ('red', [1])])
>>> dd['a']
[]
```

##### dict.items() 将 dict 类型转换成 tuple 元组类型
```python
>>> dd
defaultdict(<class 'list'>, {'yellow': [1, 3], 'blue': [2, 4], 'red': [1], 'a': []})
>>> dd.items()
dict_items([('yellow', [1, 3]), ('blue', [2, 4]), ('red', [1]), ('a', [])])
>>> 
```

#### os.open(file, flags[, mode])
###### 以可读可写方式打开文件 file, 并获得相应的权限
```python
param file  :要打开的文件
param flags :该参数可以是以下选项，多个使用 "|" 隔开：
#os.O_RDONLY:   以只读的方式打开
#os.O_WRONLY:   以只写的方式打开
#os.O_RDWR:     以读写的方式打开
#os.O_NONBLOCK: 打开时不阻塞
#os.O_APPEND:   以追加的方式打开
#os.O_CREAT:    创建并打开一个新文件
#os.O_TRUNC:    打开一个文件并截断它的长度为零（必须有写权限）
#os.O_EXCL:     如果指定的文件存在，返回错误
#os.O_SHLOCK:   自动获取共享锁
#os.O_EXLOCK:   自动获取独立锁
#os.O_DIRECT:   消除或减少缓存效果
#os.O_FSYNC :   同步写入
#os.O_NOFOLLOW: 不追踪软链接
param mode : 类似 chmod()。
#stat.S_IXOTH: 其他用户有执行权0o001
#stat.S_IWOTH: 其他用户有写权限0o002
#stat.S_IROTH: 其他用户有读权限0o004
#stat.S_IRWXO: 其他用户有全部权限(权限掩码)0o007
#stat.S_IXGRP: 组用户有执行权限0o010
#stat.S_IWGRP: 组用户有写权限0o020
#stat.S_IRGRP: 组用户有读权限0o040
#stat.S_IRWXG: 组用户有全部权限(权限掩码)0o070
#stat.S_IXUSR: 拥有者具有执行权限0o100
#stat.S_IWUSR: 拥有者具有写权限0o200
#stat.S_IRUSR: 拥有者具有读权限0o400
#stat.S_IRWXU: 拥有者有全部权限(权限掩码)0o700
#stat.S_ISVTX: 目录里文件目录只有拥有者才可删除更改0o1000
#stat.S_ISGID: 执行此文件其进程有效组为文件所在组0o2000
#stat.S_ISUID: 执行此文件其进程有效用户为文件所有者0o4000
#stat.S_IREAD: windows下设为只读
#stat.S_IWRITE: windows下取消只读

fd = os.open(file, os.O_RDWR | os.O_CREAT, stat.S_IRUSR | stat.S_IWUSR)
```

#### fcntl
```python
#int fcntl(int fd, int cmd);
#int fcntl(int fd, int cmd, long arg);
#int fcntl(int fd, int cmd, struct flock *lock);

#flags = fcntl.fcntl(fd, cmd, ...)

#fcntl()针对(文件)描述符提供控制。参数fd是被参数cmd操作(如下面的描述)的描述符。
 针对cmd的值，fcntl能够接受第三个参数int arg。
#fcntl()的返回值与命令有关。如果出错，所有命令都返回－1，如果成功则返回某个其他值
#下列三个命令有特定返回值:F_DUPFD , F_GETFD , F_GETFL以及F_GETOWN。
#                     F_DUPFD   返回新的文件描述符
#                     F_GETFD   返回相应标志
#                     F_GETFL , F_GETOWN   返回一个正的进程ID或负的进程组ID

#fcntl函数有5种功能：
#1. 复制一个现有的描述符(cmd=F_DUPFD).
#2. 获得／设置文件描述符标记(cmd=F_GETFD或F_SETFD).
#3. 获得／设置文件状态标记(cmd=F_GETFL或F_SETFL).
#4. 获得／设置异步I/O所有权(cmd=F_GETOWN或F_SETOWN).
#5. 获得／设置记录锁(cmd=F_GETLK , F_SETLK或F_SETLKW).
#1. cmd值的F_DUPFD ：
#F_DUPFD    返回一个如下描述的(文件)描述符：
#·最小的大于或等于arg的一个可用的描述符
#·与原始操作符一样的某对象的引用
#·如果对象是文件(file)的话，则返回一个新的描述符，这个描述符与arg共享相同的偏移量
  (offset)
#·相同的访问模式(读，写或读/写)
#·相同的文件状态标志(如：两个文件描述符共享相同的状态标志)
#·与新的文件描述符结合在一起的close-on-exec标志被设置成交叉式访问execve(2)的系
  统调用
#2. cmd值的F_GETFD和F_SETFD：
#F_GETFD    取得与文件描述符fd联合的close-on-exec标志，类似FD_CLOEXEC。如果
            返回值和FD_CLOEXEC进行与运算结果是0的话，文件保持交叉式访问exec()，
            否则如果通过exec运行的话，文件将被关闭(arg 被忽略)
#F_SETFD    设置close-on-exec标志，该标志以参数arg的FD_CLOEXEC位决定，应当了
            解很多现存的涉及文件描述符标志的程序并不使用常数 FD_CLOEXEC，而是将
            此标志设置为0(系统默认，在exec时不关闭)或1(在exec时关闭)
#在修改文件描述符标志或文件状态标志时必须谨慎，先要取得现在的标志值，然后按照希望修
 改它，最后设置新标志值。不能只是执行F_SETFD或F_SETFL命令，这样会关闭以前设置的标
 志位。

#  fcntl.lockf(fd, cmd, len=0, start=0, whence=0) 给文件fd加锁。
#  cmd为锁的类型:
#       LOCK_UN - 解锁
#       LOCK_SH - 获取共享锁
#       LOCK_EX - 获取独占锁
#       LOCK_NB - 避免阻塞
#  len是要锁定的字节数，start是锁定开始的字节偏移量.
#  whence 与 io.IOBase.seek()一样，具体为：
#       0 - 相对于文件的开头  （os.SEEK_SET）
#       1 - 相对于当前缓冲位置（os.SEEK_CUR）
#       2 - 相对于文件结尾   （os.SEEK_END）

```

#### os.ftruncate(fd, length)
###### 将文件fd裁剪成length大小，0也就意味着清空

#### exit()
```
sys.exit()会引发一个异常：SystemExit，如果这个异常没有被捕获，那么python解释器
将会退出。如果有捕获此异常的代码，那么这些代码还是会执行。捕获这个异常可以做一些额外
的清理工作。0为正常退出，其他数值（1-127）为不正常，可抛异常事件供捕获sys.exit()
一般用于主线程退出，os._exit()用于fork出的的子进程中退出.
```

#### signal
```python
    signal.SIGABORT
    signal.SIGHUP  # 连接挂断
    signal.SIGILL  # 非法指令
    signal.SIGINT  # 连接中断
    signal.SIGKILL # 终止进程（此信号不能被捕获或忽略）
    signal.SIGQUIT # 终端退出
    signal.SIGTERM # 终止
    signal.SIGALRM # 超时警告
    signal.SIGCONT # 继续执行暂停进程
```
###### singnal.signal(signalnum, handler) 预设(register)信号处理函数
```
signalnum为某个信号，handler为该信号的处理函数。我们在信号基础里提到，进程可以无
视信号，可以采取默认操作，还可以自定义操作。当handler为signal.SIG_IGN时,信号被
无视(ignore).当handler为singal.SIG_DFL,进程采取默认操作(default).当handler
为一个函数名时,进程采取函数中定义的操作.
```
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import signal

def handler_sig(signum, _):
    if signum == signal.SIGINT:
        print('recv signal SIGINT. Ctrl+C')
    elif signum == signal.SIGTERM:
        print('recv signal SIGTERM. ')
        sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler_sig)
    signal.signal(signal.SIGTERM, handler_sig)
    pid = os.getpid()
    for i in range(100000):
        print('i=', i)
        if i == 20:
            os.kill(pid, signal.SIGTERM)

```
```python
>>> 
======= RESTART: /Users/xiangqian5/OpenSourceSoft/shadowsocks/tttt.py =======
i= 0
i= 1
i= 2
i= 3
i= 4
i= 5
i= 6
i= 7
i= 8
i= 9
i= 10
i= 11
i=recv signal SIGINT. Ctrl+C
 12
i= 13
i= 14
i= 15
i= 16
i= 17
i= 18
i= 19
i= 20
recv signal SIGTERM. 
>>> 
```
###### signal.alarm(seconds) 定时发出SIGALRM信号
```python
def handle_alarm(signum, _):
    if signum == signal.SIGALRM:
        print('recv SIGALRM')
        sys.exit(0)
        
def test2():
    signal.signal(signal.SIGALRM, handle_alarm)
    signal.alarm(1)
    while True:
        print('not yet exit')

if __name__ == '__main__':
    test2()

```
```python
======= RESTART: /Users/xiangqian5/OpenSourceSoft/shadowsocks/tttt.py =======
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exit
not yet exitrecv SIGALRM
>>> 
```

### fork()/getpid()/getppid()/setsid()
```python
os.fork()创建子进程，父进程中返回值是子进程的pid，子进程返回值是0

os.getppid()用于子进程获取自己父进程的pid

os.getpid()进程获取自己的pid

os.setsid()
setsid做三个操作：
   1. 调用进程成为新会话的首进程，
   2. 调用进程成为新进程组的组长（组长ID就是调用进程ID），
   3. 没有控制终端
   如果调用系统函数setsid的进程是进程组组长的话，将会报错
```
