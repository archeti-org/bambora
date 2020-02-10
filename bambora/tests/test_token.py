# -*- coding: utf-8 -*-
import pytest

import os
from bambora import Bambora
from bambora.objects import Token
from datetime  import datetime, timedelta
from bambora import exceptions

from .fixtures import bambora_env

def get_test_card_valid():
    year = (datetime.now() + timedelta(days=365*2)).strftime('%y')
    card = {
        'number': "4030000010001234",
        'expiry_month': "10",
        'expiry_year': year,
        'cvd': "123"
    }

    return card

def get_test_card_invalid():
    year = (datetime.now() + timedelta(days=-365*2)).strftime('%y')
    card = {
        'number': "4030000010001234",
        'expiry_month': "10",
        'expiry_year': year,
        'cvd': "321"
    }
    return card

def test_token_creation(bambora_env):
    token = bambora_env.tokens.create(get_test_card_valid())

    assert os.environ.get('BAMBORA_MERCHANT_ID') is not None
    assert isinstance(token, Token)
    assert isinstance(token._attrs.get('token'), str)
    assert isinstance(token._attrs.get('token'), str)
    assert isinstance(token._attrs.get('version'), int)
    assert isinstance(token._attrs.get('message'), str)

    assert len(token._attrs.keys()) == 4


def test_create_profile(bambora_env):
    token = bambora_env.tokens.create(get_test_card_valid())
    profile = bambora_env.profiles.create({
        'token': {
            'name': 'Test',
            'code': token.token
        },
        'language': 'fr'
    })

    assert profile is not None

    cards = profile.cards.list()

    assert len(cards) == 1

    payment = bambora_env.payments.create({
        "order_number": "Test Trans (%s)" % (datetime.now().strftime('%Y%m%d%H%M%S%f'),),
        "amount": 20,
        "payment_method": "payment_profile",
        "payment_profile": {
            "customer_code": profile.customer_code,
            "card_id": cards[0].get_id()
        }
    })

    assert payment is not None

    trans1 = cards[0].delete()

    cards2 = profile.cards.list()

    assert len(cards2) == 0

    trans2 = profile.delete()

    with pytest.raises(exceptions.NotFoundError):
        trans3 = profile.delete()
