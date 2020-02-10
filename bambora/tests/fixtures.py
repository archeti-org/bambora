# -*- coding: utf-8 -*-
import pytest
import os


@pytest.fixture
def bambora_env():
    from bambora import Bambora
    payment_profile = os.environ.get('PAYMENT_PROFILE_PASSCODE') 
    payment_report = os.environ.get('PAYMENT_REPORT_PASSCODE') 
    payment_gateway = os.environ.get('PAYMENT_GATEWAY_PASSCODE') 
    merchant_id = os.environ.get('BAMBORA_MERCHANT_ID')

    return Bambora({
        "merchant_id": merchant_id,
        "url": "https://api.na.bambora.com",
        "codes": {
            "payment_passcode": payment_gateway,
            "payment_profile_passcode": payment_profile,
            "report_passcode": payment_report,
        }
    })
