import datetime
import os.path
import logging
import string
import fileHandler as fH
from requests import post, exceptions
import globalParamters


class keycloackHandler:
    """This class helps to reload the token only when neccessary. and stores it in a class variable
    """

    def __init__(self) -> None:
        self._logging = logging.getLogger(__name__)

        self.KEYCLOAK_HOST_FULL = f"{globalParamters.CONF['keycloack_host']}{globalParamters.CONF['keycloack_realm']}"
        self._logging.debug(f"KEYCLOAK_HOST_FULL: {self.KEYCLOAK_HOST_FULL}")
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.data = {
            'grant_type': 'client_credentials',
            'client_id': globalParamters.CONF['client_id'],
            'client_secret': globalParamters.CONF['client_secret']
        }
        self._token = {}
        pass


    def get_token(self) -> string:
        """This function will retreive a valid token from the Catena-X environment and returns it.

        :raises SystemExit: when the request fails a SystemExit Exception will be raised
        :return: returns a valid token
        :rtype: string
        """
        _get_token = False
        
        if self._token == {}:
            _get_token = True
        
        if  'access_token_expiry' in self._token:
            if self._token['access_token_expiry'] <= datetime.datetime.now():
                _get_token = True

        if _get_token:
            self._logging.debug('REFRESH TICKET')
            try:
                if globalParamters.USE_PROXY == True:
                    self._logging.debug('Get Token via Proxy')
                    req = post(self.KEYCLOAK_HOST_FULL, data=self.data,
                               headers=self.headers, proxies=globalParamters.CONF['proxies'])
                else:
                    self._logging.debug('Get Token without Proxy')
                    req = post(self.KEYCLOAK_HOST_FULL,
                               data=self.data, headers=self.headers)
            except exceptions.RequestException as e:
                self._logging.error(e)
                raise SystemExit()

            self._token = req.json()
            self._token['access_token_expiry'] = datetime.datetime.now(
            ) + datetime.timedelta(seconds=+self._token['expires_in'])

            self._logging.debug(
                f"  new_expiry: {self._token['access_token_expiry']}")

        return self._token['access_token']
