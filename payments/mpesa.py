import base64
from datetime import datetime

import requests
from decouple import config

DARAJA_BASE_URL = config('DARAJA_BASE_URL', default='https://sandbox.safaricom.co.ke')
CONSUMER_KEY = config('DARAJA_CONSUMER_KEY', default='')
CONSUMER_SECRET = config('DARAJA_CONSUMER_SECRET', default='')
SHORTCODE = config('DARAJA_SHORTCODE', default='')
PASSKEY = config('DARAJA_PASSKEY', default='')
CALLBACK_URL = config('DARAJA_CALLBACK_URL', default='')


def get_access_token():
    resp = requests.get(
        f'{DARAJA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials',
        auth=(CONSUMER_KEY, CONSUMER_SECRET),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()['access_token']


def stk_push(phone_number, amount, account_reference, description):
    """Initiates a Daraja STK Push prompt on the customer's phone.
    Returns the raw Daraja response dict (contains CheckoutRequestID)."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f'{SHORTCODE}{PASSKEY}{timestamp}'.encode()).decode()
    token = get_access_token()

    payload = {
        'BusinessShortCode': SHORTCODE,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': int(amount),
        'PartyA': phone_number,
        'PartyB': SHORTCODE,
        'PhoneNumber': phone_number,
        'CallBackURL': CALLBACK_URL,
        'AccountReference': account_reference,
        'TransactionDesc': description,
    }
    resp = requests.post(
        f'{DARAJA_BASE_URL}/mpesa/stkpush/v1/processrequest',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
