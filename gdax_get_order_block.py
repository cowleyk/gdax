import requests


from nio.properties import StringProperty, BoolProperty
from nio.block.base import Signal

from .gdax_base_block import GdaxBase, GDAXRequestAuth

class GdaxGetOrder(GdaxBase):

    sandbox = BoolProperty(title='Use sandbox account?', default=True)
    order_id = StringProperty(title='Order ID', default='UUID of order')

    def process_signals(self, signals):
        for signal in signals:
            url = 'https://api-public.sandbox.gdax.com/orders/' if self.sandbox() else 'https://api.gdax.com/orders'
            auth = GDAXRequestAuth(self.api_key(), self.api_secret(), self.passphrase())
            response = requests.post(url + self.order_id(signal), auth=auth)
            self.notify_signals([Signal(response.json())])
