"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from freeswitch import consoleLog
import shlex


def usage():
    res = "Usage: python PCARI_Parse_SMS_Body"
    return res


def parse(args):
    res = shlex.split(args)
    s = [
        'GSEND',
        'GCREATE',
        'GDELETE',
        'GADDMEM',
        'GDELMEM',
        'GUNJOIN',
        'GROUP']
    if res[0].upper() in s:
        res[0] = res[0].upper()
    else:
        for i in range(0, len(res)):
            res[i] = res[i].upper()
    return (len(res), res)


def chat(message, args):
    (len, f) = parse(args)
    if (f):
        consoleLog('info', "Returned Chat: " + str(f) + "\n")
        message.chat_execute('set', '_len=%d' % len)
        for i in range(0, len):
            value = str(f[i]).strip()  # we know it is a string!
            #            if (i == 0):
            #                value = value.upper()
            varname = 'data_' + str(i)
            consoleLog('info', "Return Chat: " + varname + "=" + value + "\n")
            message.chat_execute('set', '%s=%s' % (varname, value))
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
