import types


# The resource locator
class A:
    def __init__(self):
        A.resources = {}
        B(self)
        C(self)

    # Add resource to collection
    def add(self, name, B):
        A.resources[name] = B

    # Mess with everything
    def talk(self):
        print(A.resources)
        for key in A.resources:
            A.resources[key].hello()

    def register(resource):
        def find(resource, name):
            return A.resources[name]

        resource.method = types.MethodType(find, resource)


# Base class for proof
class B(object):
    def __init__(self, A):
        A.add('B', self);

    def hello(self):
        print ("Hi I am B")

    # Create a find function


# Can inject child/friend classes
class C(B):
    def __init__(self, A):
        A.add('C', self)

    def hello(self):
        print ("Hi I am C")


a = A()
a.talk()
