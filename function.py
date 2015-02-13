import subprocess

def executeSystemCommand(cmd, inp = None):
    """ Executes a system command and returns the output. """

    if not inp:
        output = ''.join(subprocess.check_output(cmd, stderr = subprocess.STDOUT))
    else:
        p = subprocess.Popen(cmd, stdin = subprocess.PIPE,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT)

        output = ''.join(p.communicate(input = inp)[0])

    return output

class FunctionBase:
    """ This class contains basic data and data management functions. It is inherited
        by Function and FunctionPrototype."""

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
            if v.value != value:
                v.hasChanged = True

            v.value = value
        else:
            print 'Value %s does not exist' % name

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
    """ This class is inherited to describe how a function works and what input and output
        values it has. The actual function instances are of class Function. """

    def __init__(self, name):

        FunctionBase.__init__(self, name)

    def execute(self):

        return

class Function(FunctionBase):
    """ This is an instance of a function, with its own input and output data. """

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

        for v in self.inputValues + self.outputValues + self.subnetInputValues + self.subnetOutputValues:
            v.owner = self
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
            if self.functionPrototype.execute():
                self.resetInputChange()