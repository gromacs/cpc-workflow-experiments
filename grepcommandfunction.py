from value import *
from function import FunctionPrototype, executeSystemCommand

class GrepCommandFunction(FunctionPrototype):

    def __init__(self, name = None):

        FunctionPrototype.__init__(self, name)

        if name == None:
            self.name = 'grepCommandFunction'

        self.inputValues        = [ListValue([], 'file_list', self), StringValue(None, 'pattern', self)]
        self.outputValues       = [StringValue(None, 'grep_output', self)]
        self.subnetInputValues  = []
        self.subnetOutputValues = []
        self.isFinished         = False

    def execute(self):

        if self.isFinished:
            print 'Finished'
            return

        file_list = self.getInputValueContainer('file_list')
        pattern   = self.getInputValueContainer('pattern')
        output    = self.getOutputValueContainer('grep_output')
        if file_list != None and file_list.value and pattern and pattern.value and output != None:
            input_files = []
            for f in file_list.value:
                input_files.append(f.value)
            output.value = executeSystemCommand(['grep', "%s" % pattern.value] + input_files)
            self.isFinished = True
