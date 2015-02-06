#!/usr/bin/python

from value import Value

v = Value(8, int, name='testValue')
v2 = Value(0, int, name='new')
v3 = Value([Value(1, int, name='array'), Value(2, int, name='array'), Value(3, int, name='array')], list, name='list_test')
v4 = Value([], list, name='empty_list')

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
v3.value.append(Value(4, int, name='array'))

print 'Changing first value in list %s' % v3.name
v3.value[0] = Value(2, int, name='array')

print 'Setting whole list %s' % v3.name
v3.value = [Value(1, int, name='array'), Value(2, int, name='array')]

print v3.value
print v4.value
