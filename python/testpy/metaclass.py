#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NoInstance(type):
    def __call__(self, *args):
        raise TypeError("Can't instantiate directly")


class Spam(metaclass=NoInstance):
    @staticmethod
    def grok(x):
        print('Spam.grok')

class SingletonMetaClass(type):
    def __init__(self, *args, **kwargs):
        print('SingletonMetaClass __init__.')
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        print('SingletonMetaClass __call__.')
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance

    def __new__(cls, name, bases, attrs):
        print('SingletonMetaClass __new__.')
        return type.__new__(cls, name, bases, attrs)

class Single(metaclass=SingletonMetaClass):
    def __init__(self):
        print('Creating Single.')

def test1():
    Spam.grok(33)
    spam = Spam(1)

def test():
    a = Single()

if __name__ == '__main__':
    test()
