"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import requests
import web
import xml.dom.minidom as xml

from math import ceil

from ccm.common import logger
from core import events
from core import billing
from core.subscriber import subscriber

IMSI_PREFIX = "IMSI"


def get_tag_text(nodelist):
    """ Get the text value of an XML tag (from the minidom doc)
    """
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


class cdr(object):
    def GET(self):
        raise web.NotFound()

    def POST(self):
        data = web.input()
        if "cdr" in data:
            self.process_cdr(data.cdr)
            headers = {
                'Content-type': 'text/plain'
            }
            raise web.OK(None, headers)
        raise web.BadRequest()

    def process_cdr(self, cdr_xml):
        """Processes the XML CDR for the caller."""
        cdr_dom = xml.parseString(cdr_xml)
        # Handle only b-legs for billing.
        origin = cdr_dom.getElementsByTagName("origination")
        if origin:
            return
        # Handle only b-legs for billing.
        # For our purposes, billsec is how long the call lasted. call_duration
        # captures the amount of time spent ringing, which we don't charge for,
        # so don't include here. Caller and callee are just used for logging
        # and reason statements.
        # TODO(matt): what happens if the tag does not exist?
        call_duration = int(get_tag_text(
            cdr_dom.getElementsByTagName("duration")[0].childNodes))
        billsec = int(get_tag_text(
            cdr_dom.getElementsByTagName("billsec")[0].childNodes))
        try:
            tariff = int(get_tag_text(
                cdr_dom.getElementsByTagName("call_tariff")[0].childNodes))
        except BaseException:
            pass  # pass for now
        # In b-leg cdrs, there are multiple destinations -- the sip one (IMSI)
        # and the dialed one (MSISDN).  We want the latter.
        callees = cdr_dom.getElementsByTagName("destination_number")
        callee = ''
        for c in callees:
            c = get_tag_text(c.childNodes)
            # NOT THE IMSI
            if c[0:4] != IMSI_PREFIX:
                callee = c
                break
        if callee[0] == "+":
            callee = callee[1:]
        # This is where we get the info we need to do billing.
        if len(cdr_dom.getElementsByTagName("service_type")) > 0:
            service_type = get_tag_text(
                cdr_dom.getElementsByTagName("service_type")[0].childNodes)
            service_type_orig = service_type
            promo_type = service_type[:1]
            if promo_type in ['D', 'U', 'B', 'G']:
                service_type = service_type[2:]
            # Get caller / callee info.  See the 'CDR notes' doc in drive for
            # more info.
            from_imsi, from_number, to_imsi, to_number = 4 * [None]
            # We always get 'from_imsi' from the <username> tag with the
            # <caller_profile> parent element. If it's a BTS-originated call,
            # this will be an IMSI; otherwise, it'll be an MSISDN.
            if service_type not in ['incoming_call']:
                elements = cdr_dom.getElementsByTagName('username')
                for element in elements:
                    if element.parentNode.nodeName == 'caller_profile':
                        username = get_tag_text(element.childNodes)
                        from_imsi = subscriber.get_imsi_from_username(username)
                        break
            # Get 'from_number' (only available for outside and local calls).
            if service_type in [
                'outside_call',
                'local_call',
                'incoming_call',
                    'globe_call']:
                elements = cdr_dom.getElementsByTagName('caller_id_name')
                for element in elements:
                    if element.parentNode.nodeName == 'caller_profile':
                        from_number = get_tag_text(element.childNodes)
                        break
            # Get 'to_imsi' (only available for local/incoming calls).
            if service_type in ['local_call', 'incoming_call']:
                elements = cdr_dom.getElementsByTagName('callee_id_number')
                for element in elements:
                    if element.parentNode.nodeName == 'caller_profile':
                        callee_id = get_tag_text(element.childNodes)
                        if callee_id[0:4] == IMSI_PREFIX:
                            to_imsi = callee_id
                        else:
                            # callee_id_number in the CDR is MSISDN.
                            to_imsi = subscriber.get_imsi_from_number(
                                callee_id)
                        break

            # Get 'to_number' (slightly different for local/incoming calls).
            if service_type in [
                'outside_call',
                'free_call',
                'error_call',
                    'globe_call']:
                elements = cdr_dom.getElementsByTagName('destination_number')
                for element in elements:
                    if element.parentNode.nodeName == 'caller_profile':
                        to_number = get_tag_text(element.childNodes)
                        break
            elif service_type in ['local_call', 'incoming_call']:
                elements = cdr_dom.getElementsByTagName('destination_number')
                for element in elements:
                    if (element.parentNode.nodeName ==
                            'originator_caller_profile'):
                        to_number = get_tag_text(element.childNodes)
                        break
            # Generate billing information for the caller, if the caller is
            # local to the BTS.
            if service_type != 'incoming_call':
                # remove this as tariff should have been included in curl call
                # to this endpoint
                # tariff = billing.get_service_tariff(
                #     service_type, 'call', destination_number=to_number)
                if service_type == 'globe_call':
                    service_type_temp = 'outside_call'
                else:
                    service_type_temp = service_type
                cost = billing.get_call_cost(billsec, service_type_temp,
                                             destination_number=to_number,
                                             tariff=tariff)
                reason = "%s sec call to %s (%s)" % (
                    billsec, to_number, service_type_orig)
                old_balance = subscriber.get_account_balance(from_imsi)
                subscriber.subtract_credit(from_imsi, str(cost))
                owner_imsi = from_imsi
                kind = service_type
                events.create_call_event(
                    owner_imsi, from_imsi, from_number, to_imsi, to_number,
                    old_balance, cost, kind, reason, tariff, call_duration,
                    billsec)
                # call promo/deduct to deduct bulk promo credits
                if promo_type == 'B':
                    api_url = 'http://127.0.0.1:7000/api/promo/deduct'
                    params = {
                        "imsi": owner_imsi,
                        "trans": service_type_orig,
                        # round up to nearest minute
                        "amount": int(ceil(int(billsec) / 60.0))
                    }
                    requests.post(api_url, data=params)

            # Create a call record for the callee, if applicable.
            if service_type in ['local_call', 'incoming_call']:
                if service_type == 'local_call':
                    service_type = 'local_recv_call'
                tariff = billing.get_service_tariff(service_type, 'call')
                cost = billing.get_call_cost(billsec, service_type)
                reason = "%d sec call from %s (%s)" % (
                    billsec, from_number, service_type)
                # Note! This is different than how we bill for a caller --
                # we're deducting from the 'to_imsi' (the callee) instead.
                old_balance = subscriber.get_account_balance(to_imsi)
                subscriber.subtract_credit(to_imsi, str(cost))
                owner_imsi = to_imsi
                kind = service_type
                events.create_call_event(
                    owner_imsi, from_imsi, from_number, to_imsi, to_number,
                    old_balance, cost, kind, reason, tariff, call_duration,
                    billsec)

        else:
            username = get_tag_text(
                cdr_dom.getElementsByTagName("username")[0].childNodes)
            from_imsi = subscriber.get_imsi_from_username(username)
            message = "No rate info for this call. (from: %s, billsec: %s)" % (
                from_imsi, billsec)
            logger.error(message)
