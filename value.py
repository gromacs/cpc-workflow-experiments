from notify.all import *

class Value(Variable):

    def __init__(self, initialValue, valueType, parent=None, owner=None,
                 name=None, createObject=None, fileList=None,
                 sourceTag=None):

        Variable.__init__(self, initialValue)

        self.valueType = valueType
        self.parent = parent
        self.owner = owner
        self.name = name
        if createObject is None:
            self.createObject = Value
        else:
            self.createObject = createObject
        self.fileList = fileList
        self.sourceTag = sourceTag

    def setByConnection(self, value, fromValue):

        print 'Setting %s to %s since %s changed' % (self.name, value, fromValue.name)
        self.value = value

    def addConnection(self, toValue):

        self.changed.connect_safe(toValue.setByConnection, fromValue=self)

    def removeConnection(self, toFunction):

        self.changed.disconnect_all(toFunction, fromValue=self)