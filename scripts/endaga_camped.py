"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from freeswitch import consoleLog

from core.exceptions import SubscriberNotFound
from core.subscriber import subscriber
from core.bts import bts

access_period = 0  # if not defined, defaults to 0
auth = 1  # if not defined, defaults to 2


def chat(message, msisdn):
    """Handle chat requests.

    Args:
      msisdn: a subscriber's number
    """
    try:
        imsi = str(subscriber.get_imsi_from_number(msisdn))
    except SubscriberNotFound:
        # If the MSISDN isn't even in the sub registry, it's not camped
        consoleLog('info', "Returned Chat: FALSE\n")
        message.chat_execute('set', '_openbts_ret=FALSE')
        return
    camped = [str(_['IMSI']) for _ in
              bts.get_camped_subscribers(access_period, auth)]
    res = "TRUE" if imsi[4:] in camped else "FALSE"
    consoleLog('info', "Returned Chat: %s\n" % res)
    message.chat_execute('set', '_openbts_ret=%s' % res)


def fsapi(session, stream, env, msisdn):
    """Handle FS API requests.

    Args:
      msisdn: a subscriber's number
    """
    try:
        imsi = str(subscriber.get_imsi_from_number(msisdn))
    except SubscriberNotFound:
        # If the MSISDN isn't even in the sub registry, it's not camped
        consoleLog('info', "Returned FSAPI: FALSE\n")
        stream.write('FALSE')
        return
    camped = [str(_['IMSI']) for _ in
              bts.get_camped_subscribers(access_period, auth)]
    res = "TRUE" if imsi[4:] in camped else "FALSE"
    consoleLog('info', "Returned FSAPI: %s\n" % res)
    stream.write(res)
