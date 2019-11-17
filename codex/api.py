import json
import requests
import urllib.parse
from .signer import CodexAPIRequestSigner
from .exceptions import *


class CodexExchangeAPI:

    def __init__(self, public_key: str = None, secret_key: str = None, api_base: str = 'https://api.codex.one'):
        self.__public_key = public_key
        self.__secret_key = secret_key
        self.__api_base = api_base
        self.__signer = CodexAPIRequestSigner(public_key=public_key, secret_key=secret_key)

    @staticmethod
    def __build_request_url_with_params(path: str, params: dict) -> str:
        return f'{path}?{urllib.parse.urlencode(params)}'

    def __make_request(self, path: str, method: str, payload: dict = None, sign: bool = False) -> {}:
        headers = {
            'Content-Type': 'application/json'
        }

        if sign:
            signer = self.__signer.sign(path=path)

            headers['X-Signature'] = signer['signature']
            headers['X-Public-Key'] = self.__public_key
            headers['X-Tonce'] = signer['timestamp']

        api_request = requests.request(
            method=method,
            data=json.dumps(payload) if payload is not None else '',
            url=f'{self.__api_base}{path}',
            headers=headers
        )

        try:
            api_response = api_request.json()
        except json.decoder.JSONDecodeError:
            raise CodexAPIException(
                error_description=rf'Codex Exchange returned error with code {api_request.status_code}.',
                error_message=api_request.text,
                code=api_request.status_code)

        if api_request.status_code >= 400 and api_response.get('error') is not None:
            api_error = api_response.get('error')
            raise CodexAPIException(error_description=f'Codex Exchange returned \'{api_error}\'',
                                    error_message=api_error,
                                    code=api_request.status_code)

        return api_response

    def get_info(self) -> {}:
        api_path = '/info'
        return self.__make_request(path=api_path, method='get')

    def get_tickers(self) -> {}:
        api_path = '/tickers'
        return self.__make_request(path=api_path, method='get')

    def get_trades_history(self, market: str, limit: int, ts_from: int = None, ts_to: int = None,
                           page_token: str = None) -> {}:
        api_request_params = {
            'market': str(market),
            'limit': str(limit),
        }

        if ts_from is not None:
            api_request_params['from_time'] = str(ts_from)
        if ts_to is not None:
            api_request_params['to_time'] = str(ts_to)
        if page_token is not None:
            api_request_params['page_token'] = page_token

        api_path = self.__build_request_url_with_params(path='/trades_history', params=api_request_params)
        return self.__make_request(path=api_path, method='get')

    def get_orderbook(self, market: str) -> {}:
        api_request_params = {
            'market': market
        }

        api_path = self.__build_request_url_with_params(path='/order-book', params=api_request_params)
        return self.__make_request(path=api_path, method='get')

    def get_currencies(self) -> {}:
        api_path = '/coins2/currency'
        return self.__make_request(path=api_path, method='get')

    def get_markets(self) -> {}:
        api_path = '/coins2/market'
        return self.__make_request(path=api_path, method='get')

    def get_balances(self) -> {}:
        api_path = '/balances'
        return self.__make_request(path=api_path, method='get', sign=True)

    def get_my_orders_history(self, ts_from: int, ts_to: int, limit: int, market: str = None,
                              page_token: str = None, side: str = None) -> {}:
        api_request_params = {
            'from_time': str(ts_from),
            'to_time': str(ts_to),
            'limit': str(limit)
        }

        if market is not None:
            api_request_params['market'] = market
        if page_token is not None:
            api_request_params['page_token'] = page_token
        if side is not None:
            api_request_params['side'] = side

        api_path = self.__build_request_url_with_params(path='/orders_history/my', params=api_request_params)
        return self.__make_request(path=api_path, method='get', sign=True)

    def get_my_active_orders(self, limit: int = None, order_by: str = None, ts_from: int = None, ts_to: int = None,
                             from_uuid: str = '', market: str = None, side: str = None, order_type: str = None,
                             status: str = None) -> {}:
        api_request_params = {}

        if limit is not None:
            api_request_params['limit'] = str(limit)
        if order_by is not None:
            api_request_params['order'] = order_by
        if ts_from is not None:
            api_request_params['from_time'] = str(ts_from)
        if ts_to is not None:
            api_request_params['to_time'] = str(ts_to)
        if from_uuid is not None:
            api_request_params['from_uuid'] = from_uuid
        if market is not None:
            api_request_params['market'] = market
        if side is not None:
            api_request_params['side'] = side
        if order_type is not None:
            api_request_params['type'] = order_type
        if status is not None:
            api_request_params['status'] = status

        api_path = self.__build_request_url_with_params(path='/orders/active', params=api_request_params)
        return self.__make_request(path=api_path, method='get', sign=True)

    def get_deposit_address(self, currency: str) -> {}:
        api_path = f'/coins2/api/deposit/{currency}/address'
        return self.__make_request(path=api_path, method='get', sign=True)
