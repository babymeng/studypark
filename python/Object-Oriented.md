### \_\_slots\_\_

一般情况下，创建 class 后，我们可以给 class 实例绑定任意多个属性和方法。

```python
>>> class Person(object):
	    pass

>>> person = Person()
>>> person.name = 'kekys'
>>> person.age = 50
>>> person.name
'kekys'
>>> person.age
50
>>> def get_age(self):
	    return self.age

>>> person.get_age = get_age
>>> person.get_age(person)
50
>>> 
```

但是，给实例绑定的属性和方法只作用于本实例，对其它实例不生效。

```python
>>> per2 = Person()
>>> per2.name
Traceback (most recent call last):
  File "<pyshell#30>", line 1, in <module>
    per2.name
AttributeError: 'Person' object has no attribute 'name'
>>> 
```

若要使所有实例都生效，可以给 class 进行绑定属性和方法。

```python
>>> Person.age = 40
>>> Person.name = 'kekys'
>>> 
>>> a = Person()
>>> a.name
'kekys'
>>> b = Person()
>>> b.age
40
>>> 
```

给 class 进行绑定属性和方法适用于程序运行过程中动态加载的场景。

#### 使用`__slots__`限制属性加载

 ```python
 >>> class Student(object):
	    __slots__ = ('name', 'score')

	
>>> s = Student()
>>> s.name = 'kekys'
>>> s.score = 90
>>> s.age = 60
Traceback (most recent call last):
  File "<pyshell#45>", line 1, in <module>
    s.age = 60
AttributeError: 'Student' object has no attribute 'age'
>>> 
 ```
 
 `__slots__` 仅对当前类实例起作用，对继承的子类不起作用。除非子类自身也定义`__slots__`，这样子类实例能定义的属性就是自身+父类的`__slots__`。


### @property/@func_name.setter 封装 getter/setter 方法

```python
>>> class Student(object):
	def __init__(self, name='kekys', sex='M', age=0, score=0):
		self._name = name
		self._sex = sex
		self._age = age
		self._score = score
	@property
	def score(self):
		return self._score
	@score.setter
	def score(self, score):
		if not isinstance(score, int):
			raise ValueError('score must be an integer!')
		if score < 0 or score > 100:
			raise ValueError('score must between 0 ~ 100!')
		self._score = score

		
>>> s = Student()
>>> s.score
0
>>> s.score = 60
>>> s.score
60
>>> s.score = 999
Traceback (most recent call last):
  File "<pyshell#92>", line 1, in <module>
    s.score = 999
  File "<pyshell#87>", line 15, in score
    raise ValueError('score must between 0 ~ 100!')
ValueError: score must between 0 ~ 100!
>>> 
```

### 定制类

#### \_\_str\_\_

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Student(object):
    def __init__(self, name='kekys', sex='M', age=0, score=0):
        self._name = name
        self._sex = sex
        self._age = age
        self._score = score
        
    def __str__(self):
        return "Student object (name: %s)" % self._name

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        if not isinstance(score, int):
            raise ValueError('score must be an integer!')
        if score < 0 or score > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = score

def test__str__():
    s = Student('kekys')
    print(s)        
    #无__str__:<__main__.Student object at 0x104663518>
    #有__str__:Student object (name: kekys)

if __name__ == '__main__':
    test__str__()

```

#### \_\_iter\_\_ 、 \_\_next\_\_、 \_\_getitem\_\_

`__iter__()` 返回一个迭代对象

`__next__()`返回迭代对象的下一个值。

`__getitem__()`返回迭代对象下标对应的元素，参数可以是下标，也可以是切片

```python
class Fib(object):
    def __init__(self):
        self._a = 0
        self._b = 1

    def __iter__(self):
        return self

    def __next__(self):
        self._a, self._b = self._b, self._a + self._b

        #if self._a > 1000:
            #raise StopIteration()

        return self._a

    def __getitem__(self, n):
        if isinstance(n, int):
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        elif isinstance(n, slice):
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L
            
def test__iter__():
    fib = []
    for n in Fib():
        if n > 10000:
            break
        fib.append(n)
    print("fib:", fib)
    #fib: [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    
    fib1 = Fib()
    print("fib1:", fib1[:15])
    #fib1: [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    
```

#### \_\_getattr\_\_

正常情况下，在调用类的方法或属性时，如果不存在，就会报错。此时 python解释器会尝试调用`__getattr__(self, error_attr)`来尝试获得属性。因此我们可以在`__getattr__`中进行处理获得属性。多用于动态加载或适配场景。

```python
class Student(object):
    def __init__(self, name='kekys', sex='M', age=0, score=0):
        self._name = name
        self._sex = sex
        self._age = age
        self._score = score
        
.....

>>> s = Student()
>>> s.height
Traceback (most recent call last):
  File "<pyshell#13>", line 1, in <module>
    s.height
AttributeError: 'Student' object has no attribute 'height'
>>> 
>>> def __getattr__(self, attr):
        if attr == 'height':
            return '175cm'
            
>>> Student.__getattr__ = __getattr__
>>> s.height
'175cm'
>>> 
```

下面是一个 uri 转化适配的例子：

```python
class UriChain(object):
    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return UriChain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

def testUriChain():
    print(UriChain().www.baidu.com.cn)
    #/www/baidu/com/cn
```