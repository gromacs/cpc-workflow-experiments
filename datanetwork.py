from function import Function, FunctionPrototype

class DataNetwork(object):

    def __init__(self, name=None):

        self.name = name
        self.functions = []

    def addFunction(self, function):

        assert isinstance(function, Function)

        self.functions.append(function)

    def newFunction(self, prototype, name):

        pr = prototype()

        assert isinstance(pr, FunctionPrototype), "The function prototype of the function must be of class FunctionPrototype."

        f = Function(pr, name, self)

        self.functions.append(f)

        return f

    def getAllFunctions(self):

        return self.functions

    def getFunction(self, name):

        for f in self.functions:
            if f.name == name:
                return f
