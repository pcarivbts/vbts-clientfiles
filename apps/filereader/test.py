"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from pcarifilereader import filereader

files = {"files": {"SAMPLE": "data/sample1.txt"}}
file_key = 'SAMPLE'
func = filereader.FileReader('pcari-filereader', 'INQUIRE', '200', files)
ret = func.run(file_key)
print ret

file_key = 'HELLO'
ret = func.run(file_key)
print ret
