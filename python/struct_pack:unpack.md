
### Python使用struct处理二进制
```
struct模块中最重要的三个函数是pack(), unpack(), calcsize() 

pack(fmt, v1, v2, ...) 按照给定的格式(fmt)，把数据封装成字符串(实际上是类似于c结构体的字节流)

unpack(fmt, string)    按照给定的格式(fmt)解析字节流string，返回解析出来的tuple

calcsize(fmt)          计算给定的格式(fmt)占用多少字节的内存

```  
struct中支持的格式如下表：   

```
Format    C Type                   Python            Bytes
x         pad byte                 no value            1
c         char                     string              1
b         signed char              integer             1
B         unsigned char            integer             1
?         _Bool                    bool                1
h         short                    integer             2
H         unsigned short           integer             2
i         int                      integer             4
I         unsigned int             integer or long     4
l         long                     integer             4
L         unsigned long            integer             4
q         long long                long                8
Q         unsigned long long       long                8
f         float                    float               4
d         double                   float               8
s         char[]                   string              1
p         char[]                   string              1
P         void *                   long
```
#### 【注】
```
注1.q和Q只在机器支持64位操作时有意思

注2.每个格式前可以有一个数字，表示个数

注3.s格式表示一定长度的字符串，4s表示长度为4的字符串，但是p表示的是pascal字符串

注4.P用来转换一个指针，其长度和机器字长相关

注5.最后一个可以用来表示指针类型的，占4个字节
```


*为了同c中的结构体交换数据，还要考虑有的c或c++编译器使用了字节对齐，通常是以4个字节为单位的32位系统，故而struct根据本地机器字节顺序转换.可以用格式中的第一个字符来改变对齐方式.定义如下:*  
	
	Character  Byte           order            Size and alignment
	@          native         native           凑够4个字节
	=          native         standard         按原字节数
	<          little-endian  standard         按原字节数
	>          big-endian     standard         按原字节数
	!          network        standard         按原字节数
	
使用方法是放在fmt的第一个位置，就像'@5s6sif'

```
示例一：

比如有一个结构体

struct Header

{

    unsigned short id;

    char[4] tag;

    unsigned int version;

    unsigned int count;

}
----------------------------------------------------------------------------------------------------------------------------------------
通过socket.recv接收到了一个上面的结构体数据，存在字符串s中，现在需要把它解析出来，可以使用unpack()函数.

import struct

id, tag, version, count = struct.unpack("!H4s2I", s)

上面的格式字符串中，!表示我们要使用网络字节顺序解析，因为我们的数据是从网络中接收到的，在网络上传送的时候它是网络字节顺序的.后面的H表示 一个unsigned short的id,4s表示4字节长的字符串，2I表示有两个unsigned int类型的数据.
----------------------------------------------------------------------------------------------------------------------------------------
同样，也可以很方便的把本地数据再pack成struct格式:

ss = struct.pack("!H4s2I", id, tag, version, count);

pack函数就把id, tag, version, count按照指定的格式转换成了结构体Header，ss现在是一个字符串(实际上是类似于c结构体的字节流)，可以通过 socket.send(ss)把这个字符串发送出去.
```

### Some practice
```python
>> 
>>> import struct
>>> str = struct.pack('ii', 20, 400)
>>> str
b'\x14\x00\x00\x00\x90\x01\x00\x00'
>>> len(str)
8
>>> struct.calcsize('ii')
8
>>> str = struct.pack('H4s', 4, 'a', 'b', 'c', 'd')
Traceback (most recent call last):
  File "<pyshell#13>", line 1, in <module>
    str = struct.pack('H4s', 4, 'a', 'b', 'c', 'd')
struct.error: pack expected 2 items for packing (got 5)
>>> str = struct.pack('H4s', 4, 'abcd')
Traceback (most recent call last):
  File "<pyshell#14>", line 1, in <module>
    str = struct.pack('H4s', 4, 'abcd')
struct.error: argument for 's' must be a bytes object
>>> str = struct.pack('H4s', 4, b'abcd')
>>> str
b'\x04\x00abcd'
>>> struct.calcsize('H4s')
6
>>> str = struct.pack('@H4s', 4, b'abcd')
>>> str
b'\x04\x00abcd'
>>> struct.calcsize('@H4s')
6
>>> str = struct.pack('!ii', 20, 400)
>>> str
b'\x00\x00\x00\x14\x00\x00\x01\x90'
>>> str = struct.pack('>ii', 20, 400)
>>> str
b'\x00\x00\x00\x14\x00\x00\x01\x90'
>>> str = struct.pack('<ii', 20, 400)
>>> str
b'\x14\x00\x00\x00\x90\x01\x00\x00'
>>> a, b = struct.unpack('ii', str)
>>> a
20
>>> b
400
>>> a, b = struct.unpack('<ii', str)
>>> a, b
(20, 400)
>>> a, b = struct.unpack('>ii', str)
>>> a, b
(335544320, -1878982656)
>>> print(struct.unpack('5s 4x 3s', 'test astring'))
Traceback (most recent call last):
  File "<pyshell#34>", line 1, in <module>
    print(struct.unpack('5s 4x 3s', 'test astring'))
TypeError: a bytes-like object is required, not 'str'
>>> print(struct.unpack('5s 4x 3s', b'test astring'))
(b'test ', b'ing')

>>> struct.pack_into.__doc__
'pack_into(fmt, buffer, offset, v1, v2, ...)\n\nPack the values v1, v2, ... according to the format string fmt and write\nthe packed bytes into the writable buffer buf starting at offset.  Note\nthat the offset is a required argument.  See help(struct) for more\non format strings.'
>>> 
>>> import ctypes
>>> buf = ctypes.create_string_buffer(12)
>>> buf
<ctypes.c_char_Array_12 object at 0x103e01d90>
>>> buf.raw
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
>>> struct.pack_into('iii', buf, 0, 4, 6, -1)
>>> buf.raw
b'\x04\x00\x00\x00\x06\x00\x00\x00\xff\xff\xff\xff'
>>> struct.pack_into('!iii', buf, 0, 4, 6, -1)
>>> buf.raw
b'\x00\x00\x00\x04\x00\x00\x00\x06\xff\xff\xff\xff'
>>> 
>>> buf = ctypes.create_string_buffer(13)
>>> buf.raw
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
>>> struct.pack_into('!iii', buf, 1, 4, 6, -1)
>>> buf.raw
b'\x00\x00\x00\x00\x04\x00\x00\x00\x06\xff\xff\xff\xff'
>>> a = struct.unpack_from('!iii', buf, 1)
>>> a
(4, 6, -1)
>>> 
```
