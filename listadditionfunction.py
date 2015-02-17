from value import FloatValue, ListValue
from function import FunctionPrototype

class ListAdditionFunction(FunctionPrototype):

    def __init__(self, name=None):

        FunctionPrototype.__init__(self, name)

        if name == None:
            self.name = 'additionFunction'

        self.inputValues = [ListValue(None, name='terms', ownerFunction=self,
                                      description='A list of numbers to be added',
                                      dataType=FloatValue)]
        self.outputValues = [FloatValue(None, name='sum', ownerFunction=self,
                                        description='The sum of all numbers')]
        self.isFinished = False

    def execute(self):

        if self.isFinished:
            return False

        terms = self.getInputValueContainer('terms')

        s = self.getOutputValueContainer('sum')
        #print term1, term1.value, term2, term2.value, s, s.value

        s.value = sum([t.value for t in terms.value])
        self.isFinished = True
        return True
