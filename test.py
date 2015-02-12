#!/usr/bin/python

from value import *
from function import Function
from additionfunction import AdditionFunction
from grepcommandfunction import GrepCommandFunction
from glob import glob


# First just try setting a few values and see that they can connect to each other

v = Value(8, name='testValue')
v2 = IntValue(0, name='new')
v3 = ListValue([IntValue(1, name='array'), IntValue(2, name='array'), IntValue(3, name='array')], name='list_test')
v4 = ListValue([], name='empty_list')

print 'Adding connections'
v.addConnection(v2)
v3.addConnection(v4)

print 'Setting value of %s' % v.name
v.value=10

print 'Removing connection'
v.removeConnection(v2)

print 'Setting value of %s' % v.name
v.value = 1

print 'Appending to list %s' % v3.name
v3.value.append(Value(4, name='array'))

print 'Changing first value in list %s' % v3.name
v3.value[0] = Value(2, name='array')

print 'Setting whole list %s' % v3.name
v3.value = [Value(1, name='array'), Value(2, name='array')]

print '\n\nStarting function test:'

# Test numerical add function (currently limited to two input values)

add = Function(AdditionFunction(), 'adderFunction1')
add.setInputValueContents('term1', 1)
add.setInputValueContents('term2', 2)
print '%s + %s = %s' % (add.getInputValueContents('term1'), add.getInputValueContents('term2'), add.getOutputValueContents('sum'))

add2 = Function(AdditionFunction(), 'adderFunction2')
add2.freeze()
print '\nTesting freezing function and changing input'
print add2.name, 'is frozen'
add2.setInputValueContents('term1', 2)
add2.setInputValueContents('term2', 3.5)
print '%s + %s = %s' % (add2.getInputValueContents('term1'), add2.getInputValueContents('term2'), add2.getOutputValueContents('sum'))
add2.setInputValueContents('term2', 4.5)
add2.unfreeze()
print add2.name, 'is unfrozen'
print '%s + %s = %s' % (add2.getInputValueContents('term1'), add2.getInputValueContents('term2'), add2.getOutputValueContents('sum'))

print '\nConnecting output from previous function to input of new function'
add3 = Function(AdditionFunction(), 'adderFunction3')
add.getOutputValueContainer('sum').addConnection(add3.getInputValueContainer('term1'))
add2.getOutputValueContainer('sum').addConnection(add3.getInputValueContainer('term2'))
print '%s + %s = %s' % (add3.getInputValueContents('term1'), add3.getInputValueContents('term2'), add3.getOutputValueContents('sum'))

# Test a function executing the 'grep' command

print '\nTesting grep command'
grep = Function(GrepCommandFunction(), 'grepFunction')
grep.setInputValueContents('pattern', 'class')
file_list = grep.getInputValueContainer('file_list')

if not file_list:
    print 'Cannot find file list for grep command input'
    exit(1)

files = glob('*.py')
grep.freeze()
for f in files:
    file_list.value.append(StringValue(f, None, grep))
grep.unfreeze()
print 'Output when grepping %s for "%s":' % (grep.getInputValueContents('file_list'), grep.getInputValueContents('pattern'))
print grep.getOutputValueContents('grep_output')