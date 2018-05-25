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

    def __getattr__(self, attr):
        if attr == 'height':
            return '175cm'

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

    fib1 = Fib()
    print("fib1:", fib1[:15])


class UriChain(object):
    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return UriChain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

def testUriChain():
    print(UriChain().www.baidu.com.cn)

if __name__ == '__main__':
    test__str__()
    test__iter__()
    testUriChain()
