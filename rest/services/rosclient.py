#!usr/bin/env python
#This is not a class to be used
from abc import ABCMeta

class ROSClient(object):
    __metaclass__ = ABCMeta
    def __init__(self):

    @abstractmethod
    def subscribe(self): pass
    #Subscribe target for this class

    def callback(self): pass
    #Callback method 

    @classmethod
    def __subclasshook__(cls, C)
        if cls is ROSClient:
            if any ("callback" in B.dict for B in C.__mro__):
                return true
        return 



ROSClient.register()
