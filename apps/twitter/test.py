"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import json

import requests

from pcaritwits import twits

keyword = "TWITS"
action = 'TRENDING'
param = 'PH'

service_api = 'http://127.0.0.1:7000/api/service/'
r = requests.get(service_api, params={'keyword': keyword})
service = json.loads(r.text)
name = service['name']
number = service['number']
args = service['script_arguments']
func = twits.Twits('TWITS', 'TWITS', '200', args)
ret = func.run(action, param)
print ret

action = 'TRENDING'
param = 'PH'
func = twits.Twits('TWITS', 'TWITS', '200', args)
ret = func.run(action, param)
print ret

action = 'SEARCH'
param = 'du30'
ret = func.run(action, param)
print ret

action = 'HANDLE'
param = 'cnnphilippines'
ret = func.run(action, param)
print ret
