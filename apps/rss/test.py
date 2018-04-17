"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from pcarirss import rss
import requests
import json

keyword = "RSS"
service_api = 'http://127.0.0.1:7000/api/service/'
r = requests.get(service_api, params={'keyword': keyword})
service = json.loads(r.text)
name = service['name']
number = service['number']
args = service['script_arguments']
func = rss.Rss('RSS', 'RSS', '200', args)
action = 'GMA7SHOWBIZ'
result = func.run(action)
print result

action = 'RAPPLER'
result = func.run(action)
print result
