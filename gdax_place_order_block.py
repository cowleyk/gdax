import requests
import json

from nio.properties import StringProperty, BoolProperty
from nio.block.base import Signal

from .gdax_base_block import GdaxBase, GDAXRequestAuth

class GdaxPlaceOrder(GdaxBase):

    # TODO: MAKE BASE BLOCK W/ AUTH, HAVE ORDERS, GET ORDER BLOCKS

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
