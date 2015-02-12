from value import Value

class FunctionBase:

    def __init__(self, name):

        self.name = name
        self.inputValues        = []
        self.outputValues       = []
        self.subnetInputValues  = []
        self.subnetOutputValues = []

    def getInputValueContainer(self, name):

        for v in self.inputValues:
            if v.name == name:
                return v

    def getOutputValueContainer(self, name):

        for v in self.outputValues:
            if v.name == name:
                return v

    def setInputValueContents(self, name, value):

        v = self.getInputValueContainer(name)

        if v:
            v.value = value
        else:
            print 'Value %s does not exist' % name

        if not self.frozen:
            self.execute()

    def getInputValueContents(self, name):

        v = self.getInputValueContainer(name)

        if v:
            return v.value
        else:
            print 'Value %s does not exist' % name

    def getOutputValueContents(self, name):

        v = self.getOutputValueContainer(name)

        if v:
            return v.value
        else:
            print 'Value %s does not exist' % name

class FunctionPrototype(FunctionBase):

    def __init__(self, name):

        FunctionBase.__init__(self, name)

    def execute(self):

        return

class Function(FunctionBase):

    def __init__(self, functionPrototype, name = None):

        assert functionPrototype, "A function must have a function prototype."
        assert isinstance(functionPrototype, FunctionPrototype), "The function prototype of the function must be of class FunctionPrototype."

        FunctionBase.__init__(self, name)

        self.functionPrototype  = functionPrototype
        self.frozen             = False
        self.subnetFunctions    = []
        self.inputValues        = list(functionPrototype.inputValues)
        self.outputValues       = list(functionPrototype.outputValues)
        self.subnetInputValues  = list(functionPrototype.subnetInputValues)
        self.subnetOutputValues = list(functionPrototype.subnetOutputValues)
        if name:
            self.name           = name

    def freeze(self):

        self.frozen = True

    def unfreeze(self):

        self.frozen = False
        self.execute()

    def isFrozen(self):

        return self.frozen

    def inputHasChanged(self):

        for v in self.inputValues + self.subnetInputValues:
            if v.hasChanged:
                return True

    def resetInputChange(self):

        for v in self.inputValues + self.subnetInputValues:
            v.hasChanged = False

    def execute(self):

        if not self.frozen and self.inputHasChanged():
            self.functionPrototype.execute()
            self.resetInputChange()