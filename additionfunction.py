from value import *
from function import FunctionPrototype

class AdditionFunction(FunctionPrototype):

    def __init__(self, name = None):

        FunctionPrototype.__init__(self, name)

        if name == None:
            self.name = 'additionFunction'

        self.inputValues        = [NumericValue(None, 'term1', self, 'One of the two numbers to be added'),
                                   NumericValue(None, 'term2', self, 'The second number to be added.')]
        self.outputValues       = [NumericValue(None, 'sum', self, 'The sum of the two numbers')]
        self.subnetInputValues  = []
        self.subnetOutputValues = []
        self.isFinished         = False

    def execute(self):

        if self.isFinished:
            print 'Finished'
            return False

        term1 = self.getInputValueContainer('term1')
        term2 = self.getInputValueContainer('term2')

        if not (term1.hasChanged or term2.hasChanged):
            return False

        s = self.getOutputValueContainer('sum')
        #print term1, term1.value, term2, term2.value, s, s.value
        if term1 != None and term1.value != None and term2 != None and term2.value != None and s != None:
            s.value = term1.value + term2.value
            self.isFinished = True
            return True