"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from freeswitch import consoleLog
from pcaridictionary import dictionary
import requests
import json


def usage():
    # ERRORS WERE HANDLED BY dictionary.py already
    return "Unable to process your request at the moment. Please try again later."


def parse(args):
    argss = args.split('|')
    arglen = len(argss)
    if not argss or (arglen < 1 or arglen > 3):
        return None, None, None
    else:
        return argss


def get_output(args):
    keyword, action, word = parse(args)

    service_api = 'http://127.0.0.1:7000/api/service/'
    r = requests.get(service_api, params={'keyword': keyword})
    service = json.loads(r.text)
    name = service['name']
    number = service['number']

    func = dictionary.Dictionary(name, keyword, number, None)
    ret = func.run(action, word)

    return ret


def chat(message, args):
    ret = get_output(args)
    if ret:
        consoleLog("info", "Returned Chat: " + str(ret) + "\n")
        message.chat_execute("set", "_result=%s" % str(ret))
    else:
        consoleLog("info", usage())


def fsapi(session, stream, env, args):
    ret = get_output(args)
    if ret:
        consoleLog("info", "Returned FSAPI: " + str(ret) + "\n")
        stream.write(str(ret))
    else:
        stream.write(usage())
