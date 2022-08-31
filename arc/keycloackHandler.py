import datetime
import os.path
import logging
import string
import fileHandler as fH
from requests import post, exceptions
import globalParamters


class keycloackHandler:

    def __init__(self) -> None:
        self.logging = logging.getLogger(__name__)

        self.KEYCLOAK_HOST_FULL = f"{globalParamters.CONF['keycloack_host']}{globalParamters.CONF['keycloack_realm']}"
        self.logging.debug(f"KEYCLOAK_HOST_FULL: {self.KEYCLOAK_HOST_FULL}")
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.data = {
            'grant_type': 'client_credentials',
            'client_id': globalParamters.CONF['client_id'],
            'client_secret': globalParamters.CONF['client_secret']
        }
        self.token_pickle_path = os.path.join(
            globalParamters.ROOT_DIR, globalParamters.CONF['token_pickle'])
        pass


    def get_token(self) -> string:
        _get_token = False
        _token = {}
        # _token['access_token_expiry'] = datetime.datetime.now() + \
        #     datetime.timedelta(seconds=-100)

        if os.path.isfile(self.token_pickle_path):
            self.logging.info('TOKEN LOADED FROM PICKLE')
            _token = fH.load_pickle(self.token_pickle_path)
        else:
            _get_token = True


        if _token['access_token_expiry'] <= datetime.datetime.now():
            _get_token = True

        if _get_token:
            self.logging.info('REFRESH TICKET')
            try:
                if globalParamters.USE_PROXY == True:
                    self.logging.debug('Get Token via Proxy')
                    req = post(self.KEYCLOAK_HOST_FULL, data=self.data,
                               headers=self.headers, proxies=globalParamters.CONF['proxies'])
                else:
                    self.logging.debug('Get Token without Proxy')
                    req = post(self.KEYCLOAK_HOST_FULL,
                               data=self.data, headers=self.headers)
            except exceptions.RequestException as e:
                self.logging.error(e)
                raise SystemExit()

            _token = req.json()
            _token['access_token_expiry'] = datetime.datetime.now(
            ) + datetime.timedelta(seconds=+_token['expires_in'])

            self.logging.debug(
                f"  new_expiry: {_token['access_token_expiry']}")

            fH.write_pickle(self.token_pickle_path, _token)

        return _token['access_token']
