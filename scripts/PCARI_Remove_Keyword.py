"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from freeswitch import consoleLog
import shlex


def usage():
    res = "Usage: python PCARI_Remove_Keyword"
    return res


def parse(args):
    return args.split(' ', 1)


def chat(message, args):
    (len, f) = parse(args)
    if (f):
        consoleLog('info', "Returned Chat: " + str(f) + "\n")
        message.chat_execute('set', 'actual_text=%s' % f)
    else:
        consoleLog('info', usage())


def fsapi(session, stream, env, args):
    (len, f) = parse(args)
    if (f):
        consoleLog('info', "Returned FSAPI: " + str(len) + str(f) + "\n")
        stream.write('len=' + str(len) + '\n')
        stream.write('arguments=' + str(f))
    else:
        stream.write(usage())
