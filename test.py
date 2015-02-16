#!/usr/bin/python

from value import *
from function import Function
from additionfunction import AdditionFunction
from listadditionfunction import ListAdditionFunction
from grepcommandfunction import GrepCommandFunction
from datanetwork import DataNetwork
from glob import glob


# First just try setting a few values and see that they can connect to each other

# Test numerical add function (currently limited to two input values)

network = DataNetwork()

add = network.newFunction(AdditionFunction, 'adderFunction1')
add.setInputValueContents('term1', 1)
add.setInputValueContents('term2', 2)
print '%s + %s = %s' % (add.getInputValueContents('term1'), add.getInputValueContents('term2'), add.getOutputValueContents('sum'))

add2 = network.newFunction(AdditionFunction, 'adderFunction2')
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
add3 = network.newFunction(AdditionFunction, 'adderFunction3')
add.getOutputValueContainer('sum').addConnection(add3.getInputValueContainer('term1'))
add2.getOutputValueContainer('sum').addConnection(add3.getInputValueContainer('term2'))
print '%s + %s = %s' % (add3.getInputValueContents('term1'), add3.getInputValueContents('term2'), add3.getOutputValueContents('sum'))

print '\nTesting list sum function.'
add4 = network.newFunction(ListAdditionFunction, 'listSum')
add4.setInputValueContents('terms', range(10))
print 'Sum of %s = %s' % ([fv.value for fv in add4.getInputValueContents('terms')], add4.getOutputValueContents('sum'))


print '\nTesting a whole bunch of list sum functions.'

# Generate all functions first
listarray = []
for i in range(1000):
    listarray.append(network.newFunction(ListAdditionFunction, 'listSum%d' % i))

# Connect the some of the output of the first 500 functions to the to the input of the last 500 functions.
for i in range(500, 1000):
    f = listarray[i]
    # By freezing we reduce the overall run-time by 5-10 %.
    f.freeze()
    iv = f.getInputValueContainer('terms')
    for j in range(i - 500 + 1):
        v = FloatValue()
        output = listarray[j].getOutputValueContainer('sum')
        output.addConnection(v)
        iv.append(v)

# Set the input of the the first 500 functions and print their outputs
for i in range(500):
    f = listarray[i]
    print f.name
    f.setInputValueContents('terms', range(i, i+10))
    print 'Sum of %s = %s\n' % ([fv.value for fv in f.getInputValueContents('terms')], f.getOutputValueContents('sum'))

# The input of the last 500 functions is propagated from the other 500 functions. Just print the outputs.
for i in range(500, 1000):
    f = listarray[i]
    print f.name
    f.unfreeze()
    print 'Sum of %s = %s\n' % ([fv.value for fv in f.getInputValueContents('terms')], f.getOutputValueContents('sum'))

# Test a function executing the 'grep' command

print '\nTesting grep command'
grep = network.newFunction(GrepCommandFunction, 'grepFunction')
grep.setInputValueContents('pattern', 'class')
file_list = grep.getInputValueContainer('file_list')

if not file_list:
    print 'Cannot find file list for grep command input'
    exit(1)

files = glob('*.py')
grep.freeze()
for f in files:
    file_list.value.append(StringValue(f, ownerFunction = grep))
grep.unfreeze()
print 'Output when grepping %s for "%s":' % (grep.getInputValueContents('file_list'), grep.getInputValueContents('pattern'))
print grep.getOutputValueContents('grep_output')