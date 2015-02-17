from value import StringValue, ListValue
from function import FunctionPrototype, executeSystemCommand

class GrepCommandFunction(FunctionPrototype):

    def __init__(self, name=None):

        FunctionPrototype.__init__(self, name)

        if name == None:
            self.name = 'grepCommandFunction'

        self.inputValues = [ListValue([], name='file_list', ownerFunction=self,
                                             description='List of files to search for a pattern'),
                                   StringValue(None, name='pattern', ownerFunction=self,
                                               description='The pattern to search for')]
        self.outputValues = [StringValue(None, name='grep_output', ownerFunction=self,
                                               description='The results of the search')]
        self.subnetInputValues = []
        self.subnetOutputValues = []
        self.isFinished = False

    def execute(self):

        if self.isFinished:
            print 'Finished'
            return

        file_list = self.getInputValueContainer('file_list')
        pattern = self.getInputValueContainer('pattern')
        output = self.getOutputValueContainer('grep_output')
        input_files = []
        for f in file_list.value:
            input_files.append(f.value)
        output.value = executeSystemCommand(['grep', "%s" % pattern.value] + input_files)
        self.isFinished = True
