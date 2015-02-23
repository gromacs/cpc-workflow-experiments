#!/usr/bin/python

from value import FloatValue, StringValue
from additionfunction import AdditionFunction
from listadditionfunction import ListAdditionFunction
from grepcommandfunction import GrepCommandFunction
from datanetwork import DataNetwork
from glob import glob

n_instances = 1000

# First just try setting a few values and see that they can connect to
# each other

# Test numerical add function (currently limited to two input values)

network = DataNetwork()

#print '\nTesting addition function'
#add = network.newInstance(AdditionFunction, 'adderFunction1')
#add.setInputValueContents('term1', 1)
#add.setInputValueContents('term2', 2)
#print '%s + %s = %s' % (add.getInputValueContents('term1'),
#                        add.getInputValueContents('term2'),
#                        add.getOutputValueContents('sum'))

#add2 = network.newInstance(AdditionFunction, 'adderFunction2')
#add2.freeze()
#print '\nTesting freezing function and changing input.'
#print add2.name, 'is frozen'
#add2.setInputValueContents('term1', 2)
#add2.setInputValueContents('term2', 3.5)
#print '%s + %s = %s' % (add2.getInputValueContents('term1'),
#                        add2.getInputValueContents('term2'),
#                        add2.getOutputValueContents('sum'))
#add2.setInputValueContents('term2', 4.5)
#add2.unfreeze()
#print add2.name, 'is unfrozen'
#print '%s + %s = %s' % (add2.getInputValueContents('term1'),
#                        add2.getInputValueContents('term2'),
#                        add2.getOutputValueContents('sum'))

#print '\nConnecting output from previous function to input of new function.'
## Setup the next addition function as well and connect it to output from previous functions, before add3 has even finished.
#add3 = network.newInstance(AdditionFunction, 'adderFunction3')
#add4 = network.newInstance(AdditionFunction, 'adderFunction4')
#add.getOutputValueContainer('sum').addConnection(add4.getInputValueContainer('term1'))
#add2.getOutputValueContainer('sum').addConnection(add4.getInputValueContainer('term2'))
#add3.getOutputValueContainer('sum').addConnection(add4.getInputValueContainer('term3'))

## Now connect the input for add3 (from add and add2)
#add.getOutputValueContainer('sum').addConnection(add3.getInputValueContainer('term1'))
#add2.getOutputValueContainer('sum').addConnection(add3.getInputValueContainer('term2'))
#print '%s + %s = %s' % (add3.getInputValueContents('term1'),
#                        add3.getInputValueContents('term2'),
#                        add3.getOutputValueContents('sum'))

#print '\nTesting sum with three terms, with input from previous output.'
#print '%s + %s + %s = %s' % (add4.getInputValueContents('term1'),
#                             add4.getInputValueContents('term2'),
#                             add4.getInputValueContents('term3'),
#                             add4.getOutputValueContents('sum'))

#print '\nTesting list sum function.'
#add5 = network.newInstance(ListAdditionFunction, 'listSum')
#add5.setInputValueContents('terms', range(10))
#print 'Sum of %s = %s' % ([fv.value for fv in add5.getInputValueContents('terms')],
#                          add5.getOutputValueContents('sum'))


print '\nTesting %d instances of list sum functions.' % n_instances

# Generate all functions first
listarray = []
for i in range(n_instances):
    listarray.append(network.newFunction(ListAdditionFunction, 'listSum%d' % i))

# Connect the some of the output of the first 500 functions to the to the input
# of the last 500 functions.
for i in range(n_instances/2, n_instances):
    f = listarray[i]
    # By freezing we reduce the overall run-time by 5-10 %.
    f.freeze()
    iv = f.getInputValueContainer('terms')
    for j in range(i - n_instances/2 + 1):
        v = FloatValue()
        output = listarray[j].getOutputValueContainer('sum')
        output.addConnection(v)
        iv.append(v)

# Set the input of the the first 500 functions and print their outputs
for i in range(n_instances/2):
    f = listarray[i]
    print f.name
    f.setInputValueContents('terms', range(i, i+10))
    print 'Sum of %s = %s\n' % ([fv.value for fv in f.getInputValueContents('terms')],
                                f.getOutputValueContents('sum'))

# The input of the last 500 functions is propagated from the other 500 functions. Just print the outputs.
for i in range(n_instances/2, n_instances):
    f = listarray[i]
    print f.name
    f.unfreeze()
    print 'Sum of %s = %s\n' % ([fv.value for fv in f.getInputValueContents('terms')],
                                f.getOutputValueContents('sum'))

## Test a function executing the 'grep' command

#print '\nTesting grep command'
#grep = network.newInstance(GrepCommandFunction, 'grepFunction')
#grep.setInputValueContents('pattern', 'class')
#file_list = grep.getInputValueContainer('file_list')

#if not file_list:
#    print 'Cannot find file list for grep command input'
#    exit(1)

#files = glob('*.py')
#grep.freeze()
#for f in files:
#    file_list.value.append(StringValue(f, ownerFunction=grep))
#grep.unfreeze()
#print 'Output when grepping %s for "%s":' % (grep.getInputValueContents('file_list'),
#                                             grep.getInputValueContents('pattern'))
#print grep.getOutputValueContents('grep_output')
