import types
from rest.services.singleton import Singleton
# The resource locator
@Singleton
class A:
    def __init__(self):
        A.resources = {}
        B(self)
        C(self)
    #Add resource to collection
    def add(self, name, B):
        A.resources[name] = B

    # Mess with everything
    def talk(self):
        print(A.resources)
        for key in A.resources:
            A.resources[key].hello()

    def allwave(self):
        print "B finding "
        A.resources['B'].wave('C')
        print "C finding "
        A.resources['C'].wave('B')
			

# Base class for proof
class B(object):
    def __init__(self, A):
        A.add('B', self);
        #A.register(self);

    def hello(self):
        print ("B")

    def wave(self, name):
        print A.resources[name].hello()
	#Create a find function

#Can inject child/friend classes
class C(B):
    def __init__(self, A):
        A.add('C', self)

    def hello(self):
        print ("C")

A.Instance().allwave()
