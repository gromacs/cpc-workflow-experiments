from notify.all import *
from types import *
from function import Function, FunctionPrototype

class Value(Variable):
    """ Value is a container for a generic value. It can have a name and its owner, if any,
        is the function or function prototype that it is part of. It can also have a description
        documenting what it contains. The actual value contents is stored in self.value, inheriting
        the functionality of Variable from the notify library. Values can be connected to each other
        to propagate data. """

    def __init__(self, initialValue=None, name=None, owner=None, description=''):
        """
           :param initialValue: A value of any kind that the value container should contain from the start.
           :param name        : The name of the variable.
           :param owner       : The owner of the variable.
           :type owner        : Function/FunctionPrototype.
           :param description : A description of the data and what it is used for.
           :type description  : str.
           :raises            : AssertionError.
        """

        assert owner == None or isinstance(owner, (Function, FunctionPrototype))

        Variable.__init__(self, initialValue)

        self.name = name
        self.owner = owner
        self.hasChanged = False # If the value changes this will be set to True.
        self.description = description

    def is_allowed_value(self, value):
        """ Verify that the variable is of an allowed type. Overrides method of Variable.
            The implementation in the Value base class allows all values.

           :param value: The value that should be checked if it is allowed.
           :returns:     True is the value is allowed (always) or False if it isn't (never).
        """
        return True

    def set(self, value):
        """ Set the value. This is also called when using the assignment operator (=). is_allowed_value
            is called to verify that the value is OK.

           :param value: The new value.
        """

        # If the value is changed update the hasChanged flag.
        if self.value != value:
            self.hasChanged = True

        Variable.set(self, value)

        # If the value is input to a function execute the function code (if all input is set).
        if self.owner and (self in self.owner.inputValues or self in self.owner.subnetInputValues):
            self.owner.isFinished = False
            self.owner.execute()

    def _setByConnection(self, value, fromValue):

        #print 'Setting %s to %s since %s changed' % (self.name, value, fromValue.name)
        if self.value != value:
            self.hasChanged = True

        self.value = value

        if self.owner:
            if self in self.owner.inputValues or self in self.owner.subnetInputValues:
                self.owner.isFinished = False
                self.owner.execute()

    def addConnection(self, toValue):
        """ Add a connection from this value container to another value container. When this value is
            modified the other value will reflect that.

           :param toValue: The value that should be updated when this value is updated.
        """

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

        self.changed.connect_safe(toValue._setByConnection, fromValue=self)

        if self.value != toValue.value:
            toValue.value = self.value
            toValue.hasChanged = True
            if toValue.owner:
                toValue.owner.execute()

    def removeConnection(self, toValue):
        """ Remove all connections from this value to another. toValue will no longer reflect changes
            made to this value.

           :param toValue: The value to which all connections (from this value) should be removed.
        """

        self.changed.disconnect_all(toValue, fromValue=self)

class IntValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None, description=''):

        Value.__init__(self, initialValue, name, owner, description)

    def is_allowed_value(self, value):

        if value == None or isinstance(value, IntType):
            return True
        else:
            return False

class FloatValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None, description=''):

        Value.__init__(self, initialValue, name, owner, description)

    def is_allowed_value(self, value):

        if value == None or isinstance(value, FloatType):
            return True
        else:
            return False

class NumericValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None, description=''):

        Value.__init__(self, initialValue, name, owner, description)

    def is_allowed_value(self, value):

        if value == None or isinstance(value, (IntType, FloatType)):
            return True
        else:
            return False

class StringValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None, description=''):

        Value.__init__(self, initialValue, name, owner, description)

    def is_allowed_value(self, value):

        # Allow both StringType and UnicodeType
        if value == None or isinstance(value, StringTypes):
            return True
        else:
            return False

class ListValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None, description=''):

        Value.__init__(self, initialValue, name, owner, description)

    def is_allowed_value(self, value):

        if value == None or isinstance(value, ListType):
            return True
        else:
            return False

class DictValue(Value):

    def __init__(self, initialValue=None, name=None, owner=None, description=''):

        Value.__init__(self, initialValue, name, owner, description)

    def is_allowed_value(self, value):

        if value == None or isinstance(value, DictType):
            return True
        else:
            return False

