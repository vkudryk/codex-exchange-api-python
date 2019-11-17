from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from time import time_ns
from .exceptions import CodexAPIRequestSignerException


class CodexAPIRequestSigner:
    def __init__(self, public_key: str = None, secret_key: str = None):
        self.__public_key = public_key
        self.__secret_key = secret_key

    def sign(self, path: str, json_payload: str = '') -> {str, str}:
        if self.__public_key is None or self.__secret_key is None:
            raise CodexAPIRequestSignerException(
                'Use of private API methods require public_key and secret_key to be set.')

        signing_key = SigningKey(seed=self.__secret_key[:64], encoder=HexEncoder)

        tonce_timestamp = str(time_ns())

        message = f'{json_payload}{path}{tonce_timestamp}'

        signature = signing_key.sign(message=message.encode(), encoder=HexEncoder)

        return {
            'signature': signature,
            'timestamp': tonce_timestamp
        }
