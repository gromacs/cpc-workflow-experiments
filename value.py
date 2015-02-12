from notify.all import *
from types import *

class Value(Variable):

    def __init__(self, initialValue=None, name=None, owner=None):

        Variable.__init__(self, initialValue)

        self.name = name
        self.owner = owner
        self.hasChanged = False

    def is_allowed_value(self, value):

        return True

    def set(self, value):

        if self.value != value:
            self.hasChanged = True

        Variable.set(self, value)

    def setByConnection(self, value, fromValue):

        print 'Setting %s to %s since %s changed' % (self.name, value, fromValue.name)
        if self.owner:
            if self in self.owner.inputValues or self in self.owner.subnetInputValues:
                self.owner.isFinished = False
                if not self.owner.isFrozen():
                    self.owner.execute

        if self.value != value:
            self.hasChanged = True

        self.value = value

    def addConnection(self, toValue):

        if self.owner:
            if self not in self.owner.outputValues and self not in self.owner.subnetOutputValues:
                print "Cannot add a connection from a value that is not an output value."
                return
            if self in self.owner.subnetOutputValues:
                if toValue.owner not in self.owner.subnetFunctions:
                    print "Cannot add a connection. Connected value is not part of the function subnet."
                    return
                if toValue not in toValue.owner.inputValues and toValue not in toValue.owner.subnetInputValues:
                    print "Cannot add a connection. Connected value is not part of the function subnet."
                    return

        self.changed.connect_safe(toValue.setByConnection, fromValue=self)

        if self.value != toValue.value:
            toValue.value = self.value
            toValue.hasChanged = True
            if toValue.owner:
                toValue.owner.execute()

    def removeConnection(self, toFunction):

        self.changed.disconnect_all(toFunction, fromValue=self)

class IntValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None):

        Value.__init__(self, initialValue, name, owner)

    def is_allowed_value(self, value):

        if value == None or isinstance(value, IntType):
            return True
        else:
            return False

class FloatValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None):

        Value.__init__(self, initialValue, name, owner)

    def is_allowed_value(self, value):

        if value == None or isinstance(value, FloatType):
            return True
        else:
            return False

class NumericValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None):

        Value.__init__(self, initialValue, name, owner)

    def is_allowed_value(self, value):

        if value == None or isinstance(value, (IntType, FloatType)):
            return True
        else:
            return False

class StringValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None):

        Value.__init__(self, initialValue, name, owner)

    def is_allowed_value(self, value):

        # Allow both StringType and UnicodeType
        if value == None or isinstance(value, StringTypes):
            return True
        else:
            return False

class ListValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None):

        Value.__init__(self, initialValue, name, owner)

    def is_allowed_value(self, value):

        if value == None or isinstance(value, ListType):
            return True
        else:
            return False

class DictValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None):

        Value.__init__(self, initialValue, name, owner)

    def is_allowed_value(self, value):

        if value == None or isinstance(value, DictType):
            return True
        else:
            return False

