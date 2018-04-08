# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from tests import IntegrationTestCase
from tests.holodeck import Request
from twilio.base.exceptions import TwilioException
from twilio.http.response import Response


class AssignedAddOnExtensionTestCase(IntegrationTestCase):

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .incoming_phone_numbers(sid="PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .assigned_add_ons(sid="XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .extensions(sid="XFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").fetch()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://api.twilio.com/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/IncomingPhoneNumbers/PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/AssignedAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions/XFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sid": "XFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "assigned_add_on_sid": "XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "resource_sid": "PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "friendly_name": "Incoming Voice Call",
                "product_name": "Programmable Voice",
                "unique_name": "voice-incoming",
                "uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/IncomingPhoneNumbers/PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/AssignedAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions/XFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json",
                "enabled": true
            }
            '''
        ))

        actual = self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .incoming_phone_numbers(sid="PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .assigned_add_ons(sid="XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .extensions(sid="XFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").fetch()

        self.assertIsNotNone(actual)

    def test_list_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .incoming_phone_numbers(sid="PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .assigned_add_ons(sid="XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .extensions.list()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://api.twilio.com/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/IncomingPhoneNumbers/PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/AssignedAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions.json',
        ))

    def test_read_full_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "end": 0,
                "first_page_uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/IncomingPhoneNumbers/PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/AssignedAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions.json?PageSize=50&Page=0",
                "next_page_uri": null,
                "page": 0,
                "page_size": 50,
                "previous_page_uri": null,
                "extensions": [
                    {
                        "sid": "XFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "assigned_add_on_sid": "XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "resource_sid": "PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "friendly_name": "Incoming Voice Call",
                        "product_name": "Programmable Voice",
                        "unique_name": "voice-incoming",
                        "enabled": true,
                        "uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/IncomingPhoneNumbers/PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/AssignedAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions/XFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json"
                    }
                ],
                "start": 0,
                "uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/IncomingPhoneNumbers/PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/AssignedAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions.json?PageSize=50&Page=0"
            }
            '''
        ))

        actual = self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .incoming_phone_numbers(sid="PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .assigned_add_ons(sid="XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .extensions.list()

        self.assertIsNotNone(actual)

    def test_read_empty_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "end": 0,
                "first_page_uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/IncomingPhoneNumbers/PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/AssignedAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions.json?PageSize=50&Page=0",
                "next_page_uri": null,
                "page": 0,
                "page_size": 50,
                "previous_page_uri": null,
                "extensions": [],
                "start": 0,
                "uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/IncomingPhoneNumbers/PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/AssignedAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions.json?PageSize=50&Page=0"
            }
            '''
        ))

        actual = self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .incoming_phone_numbers(sid="PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .assigned_add_ons(sid="XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .extensions.list()

        self.assertIsNotNone(actual)
