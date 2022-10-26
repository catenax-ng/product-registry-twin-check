""" Keyckloack handler manages communication with the keycloak instance
"""
import datetime
import logging
import string
from requests import post, exceptions
import global_parameters as GlobalParamters


__author__ = "Johannes Zahn"
__copyright__ = """
 Copyright (c) 2022 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
 Copyright (c) 2021,2022 Contributors to the CatenaX (ng) GitHub Organisation.

 See the NOTICE file(s) distributed with this work for additional
 information regarding copyright ownership.

 This program and the accompanying materials are made available under the
 terms of the Apache License, Version 2.0 which is available at
 https://www.apache.org/licenses/LICENSE-2.0. *
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 License for the specific language governing permissions and limitations
 under the License.

 SPDX-License-Identifier: Apache-2.0
"""
__license__ = "Apache-2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = ""
__status__ = "exploration"


class KeycloackHandler:
    """This class helps to reload the token only when neccessary. and stores it in a class variable
    """

    def __init__(self) -> None:
        self._logging = logging.getLogger(__name__)

        self.keycloack_host_full = f"{GlobalParamters.CONF['keycloack_host']}{GlobalParamters.CONF['keycloack_realm']}"

        self._logging.debug("keycloack_host_full: %s",
                            self.keycloack_host_full)

        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        self.data = {
            'grant_type': 'client_credentials',
            'client_id': GlobalParamters.CONF['client_id'],
            'client_secret': GlobalParamters.CONF['client_secret']
        }
        self._token = {}


    def get_token(self) -> string:
        """This function will retreive a valid token from the Catena-X environment and returns it.

        :raises SystemExit: when the request fails a SystemExit Exception will be raised
        :return: returns a valid token
        :rtype: string
        """
        _get_token = False

        if self._token == {}:
            _get_token = True

        if 'access_token_expiry' in self._token:
            if self._token['access_token_expiry'] <= datetime.datetime.now():
                _get_token = True

        if _get_token:
            self._logging.debug('REFRESH TICKET')
            try:
                if GlobalParamters.USE_PROXY is True:
                    self._logging.debug('Get Token via Proxy')
                    req = post(self.keycloack_host_full, data=self.data,
                               headers=self.headers, proxies=GlobalParamters.CONF['proxies'])
                else:
                    self._logging.debug('Get Token without Proxy')
                    req = post(self.keycloack_host_full,
                               data=self.data, headers=self.headers)
            except exceptions.RequestException as exc:
                self._logging.error(exc)
                raise SystemExit() from exc

            self._token = req.json()
            
            if 'error' in self._token.keys():
                self._logging.error(self._token)
                raise SystemExit()
            else:
                self._logging.debug('token %s', self._token)
                self._token['access_token_expiry'] = datetime.datetime.now(
                ) + datetime.timedelta(seconds=+self._token['expires_in'])

                self._logging.debug(
                    "  new_expiry: %s", self._token['access_token_expiry'])

        return self._token['access_token']
