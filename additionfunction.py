from value import *
from function import FunctionPrototype

class AdditionFunction(FunctionPrototype):

    def __init__(self, name = None):

        FunctionPrototype.__init__(self, name)

        if name == None:
            self.name = 'additionFunction'

        self.inputValues        = [FloatValue(None, name = 'term1', ownerFunction = self, description = 'One of the two numbers to be added'),
                                   FloatValue(None, name = 'term2', ownerFunction = self, description = 'The second number to be added.')]
        self.outputValues       = [FloatValue(None, name = 'sum', ownerFunction = self, description = 'The sum of the two numbers')]
        self.subnetInputValues  = []
        self.subnetOutputValues = []
        self.isFinished         = False

    def _execute(self):

        if self.isFinished:
            print 'Finished'
            return False

        term1 = self.getInputValueContainer('term1')
        term2 = self.getInputValueContainer('term2')

        s = self.getOutputValueContainer('sum')
        #print term1, term1.value, term2, term2.value, s, s.value
        s.value = term1.value + term2.value
        self.isFinished = True
        return True