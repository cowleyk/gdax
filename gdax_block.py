import requests
import json
import base64, hashlib, hmac, time
from requests.auth import AuthBase

from nio.block.base import Block
from nio.properties import VersionProperty, StringProperty, BoolProperty
from nio.block.base import Signal


class GdaxOrder(Block):

    version = VersionProperty('0.1.0')
    api_key = StringProperty(title='API Key', default='[[GDAX_API_KEY]]')
    api_secret = StringProperty(title='API Secret', default='[[GDAX_API_SECRET]]')
    passphrase = StringProperty(title='Passphrase', default='[[GDAX_PASSPHRASE]]')
    buy_sell = BoolProperty(title='Place sell order?', default=False)
    sandbox = BoolProperty(title='Use sandbox account?', default=True)
    product_id = StringProperty(title='Product ID', default='BTC-USD')
    size = StringProperty(title='Order Size', default='10')

    def process_signals(self, signals):
        for signal in signals:
            url = 'https://api-public.sandbox.gdax.com/orders' if self.sandbox() else 'https://api.gdax.com/orders'
            auth = GDAXRequestAuth(self.api_key(), self.api_secret(), self.passphrase())
            order_data = {
                'type': 'market',
                'side': 'sell' if self.buy_sell() else 'buy',
                'product_id': 'BTC-USD',
                'size': self.size()
            }
            response = requests.post(url, data=json.dumps(order_data), auth=auth)
            self.notify_signals([Signal(response.json())])


class GDAXRequestAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (
        request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())
        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request