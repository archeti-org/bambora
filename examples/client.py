# -*- coding: utf-8 -*-
from bambora import Bambora
from bambora.exceptions import BamboraError, APIError
import logging

from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


parser = ArgumentParser()
parser.add_argument('--merchant', help="Merchant ID")
parser.add_argument('--payment', help="Payment Passcode")
parser.add_argument('--profile', help="Profile Passcode")
parser.add_argument('--reports', help="Reports Passcode")

args = parser.parse_args()

bambora = Bambora({
    "merchant_id": args.merchant,
    "url": "https://api.na.bambora.com",
    "codes": {
        "payment_passcode":  args.payment,
        "payment_profile_passcode": args.profile,
        "report_passcode": args.reports
    }
})

token = bambora.tokens.create({
    'number': "4030000010001234",
    'expiry_month': "10",
    'expiry_year': "22",
    'cvd': "123"
})

profile = bambora.profiles.create({
    'token': {
        'name': 'Test',
        'code': token.token
    },
    'language': 'fr'
})

cards = profile.cards.list()

payment = bambora.payments.create({
    "order_number": "ABC%s" % profile.customer_code[-5:],
    "amount": 20,
    "payment_method": "payment_profile",
    "payment_profile": {
        "customer_code": profile.customer_code,
        "card_id": cards[0].get_id()
    }
})

trans1 = cards[0].delete()
trans2 = profile.delete()


reports = []
try:
    fetch_data = True
    start = 1
    end = 10

    #while fetch_data:
    #    res = bambora.reports.list({
    #        'name': 'Search',
    #        'start_date': '2018-04-22T10:03:19',
    #        'end_date': '2018-10-03T10:03:19',
    #        'start_row': start,
    #        'end_row': end
    #    })
    #    if not len(res):
    #        fetch_data = False
    #    else:
    #        start += 20
    #        end += 20
    #        reports += res

    token2 = bambora.tokens.create({
        'number': "4030000010001235",
        'expiry_month': "10",
        'expiry_year': "22",
        'cvd': "123"
    })
    profile2 = bambora.profiles.create({
        "token": {
            "name": "Some name",
            "code": token2.token
        },
        "validate": True,
    })
except BamboraError as exc:
    import pdb; pdb.set_trace()
    log.info(exc.message)

#import pdb; pdb.set_trace()
#print(bambora.profiles.get('test').get_path())
#print(bambora.profiles.get_path())
