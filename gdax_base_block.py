import base64, hashlib, hmac, time
from requests.auth import AuthBase

from nio.block.base import Block
from nio.properties import VersionProperty, StringProperty
from nio.util.discovery import not_discoverable


@not_discoverable
class GdaxBase(Block):

    version = VersionProperty('0.1.0')
    api_key = StringProperty(title='API Key', default='[[GDAX_API_KEY]]')
    api_secret = StringProperty(title='API Secret', default='[[GDAX_API_SECRET]]')
    passphrase = StringProperty(title='Passphrase', default='[[GDAX_PASSPHRASE]]')


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