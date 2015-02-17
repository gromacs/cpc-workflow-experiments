from value import FloatValue
from function import FunctionPrototype

class AdditionFunction(FunctionPrototype):

    def __init__(self, name=None):

        FunctionPrototype.__init__(self, name)

        if name == None:
            self.name = 'additionFunction'

        self.inputValues = [FloatValue(None, name='term1', ownerFunction=self,
                                       description='One of the two numbers to be added'),
                            FloatValue(None, name='term2', ownerFunction=self,
                                       description='The second number to be added.'),
                             FloatValue(None, name='term3', ownerFunction=self,
                                        optional=True,
                                        description='A third term to be added (optional).')]
        self.outputValues = [FloatValue(None, name='sum', ownerFunction=self,
                                        description='The sum of the two numbers')]
        self.isFinished = False

    def execute(self):

        if self.isFinished:
            return False

        term1 = self.getInputValueContainer('term1')
        term2 = self.getInputValueContainer('term2')
        term3 = self.getInputValueContainer('term3')

        s = self.getOutputValueContainer('sum')
        #print term1, term1.value, term2, term2.value, s, s.value
        s.value = term1.value + term2.value
        if term3.value:
            s.value += term3.value
        self.isFinished = True
        return True
