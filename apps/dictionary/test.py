"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from pcaridictionary import dictionary

d = dictionary.Dictionary('DICTIONARY', 'WORD', '200', None)
print d.instructions()

action = 'RANDOM'
param = 'dictionary'
result = d.run(action, param)
print action
print result

action = 'DEFINE'
param = 'dictionary'
result = d.run(action, param)
print action
print result

action = 'SYNONYMS'
param = 'dictionary'
result = d.run(action, param)
print action
print result

action = 'ANTONYMS'
param = 'dictionary'
result = d.run(action, param)
print action
print result
