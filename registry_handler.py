""" The Registry Handler manages all the communication with the Digital Twin Registry.
"""
import os
import logging
from enum import Enum
from time import sleep
from random import uniform
from urllib.parse import urljoin
from requests import get, exceptions
from tqdm import tqdm
import file_handler as fH
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


class Check(Enum):
    """Check Enum"""
    PASSED = 1
    FAILED = 2


class RegistryHandler:
    """Class to Handle the communication with the registry
    """

    def __init__(self, kc_h) -> None:
        self._logging = logging.getLogger(__name__)
        self.kc_h = kc_h

    def get_twin(self, aas_id):
        """Retrieves a twin for a specific aasId

        :param aasId: Asset Administration Id from a 
        :type aasId: string
        :return: twin
        :rtype: dict
        """
        try:
            get_shell = f"registry/registry/shell-descriptors/{aas_id['urn']}"
            url = urljoin(GlobalParamters.CONF['registry_url'], get_shell)
            # self._logging.debug(f'url: {url}')
            self._logging.debug('url: %s', url)
            headers = {
                'Authorization': f'Bearer {self.kc_h.get_token()}'
            }

            if GlobalParamters.USE_PROXY is True:
                req = get(url, headers=headers,
                          proxies=GlobalParamters.CONF['proxies'])
            else:
                req = get(url, headers=headers)

            # self._logging.debug(f'Request status: {req}')
            # self._logging.debug(f'Request payload: {req.json()}')
            self._logging.debug('Request status: %s',req)
            self._logging.debug('Request payload: %s',req.json())

        except exceptions.RequestException as exc:
            self._logging.error(exc)
            raise SystemExit() from exc

        return req.json()

    def get_twins_by_bpn(self, bpn):
        """Retrieves al twins for a specific bpn

        :param bpn: Business Partner Number
        :type bpn: string
        :return: twins
        :rtype: list
        """

        self._logging.info('Getting all Twins for BPN: %s',bpn)
        twins = []
        load_twin_list = False
        file_name = f"{GlobalParamters.CONF['twins_pickle_pre_name']}_{bpn['value']}.pickle"
        pickle_path = os.path.join(GlobalParamters.ROOT_DIR, file_name)

        if os.path.isfile(pickle_path):
            twins = fH.load_pickle(pickle_path, 'rb')
            # len([twin for twin in twins if twin['bpn'] == bpn['value'] ])
            # if len([twin for twin in twins if twin['bpn'] == bpn['value'] ]) == 0:
            #     self._logging.info('No values found for %s', bpn['value'] )
            #     load_twin_list = True
            # else:
            #     return [twin for twin in twins if twin['bpn'] == bpn['value'] ]
        else:
            load_twin_list = True

        self._logging.info(
            "load_twin_list: %s, pikle path: %s",load_twin_list, pickle_path)

        if load_twin_list:
            try:
                params = """assetIds=[{"key":"ManufacturerId","value":\"""" + \
                    bpn['value']+""""}]"""
                get_shells = "registry/lookup/shells"
                url = urljoin(GlobalParamters.CONF['registry_url'], get_shells)
                self._logging.debug('url: %s',url)
                headers = {
                    'Authorization': f'Bearer {self.kc_h.get_token()}',
                    'Content-Type': 'application/x-www-form-urlencoded'

                }
                if GlobalParamters.USE_PROXY is True:
                    req = get(url, params=params, headers=headers,
                              proxies=GlobalParamters.CONF['proxies'])
                else:
                    req = get(url, params=params,
                              headers=headers, proxies=None)

                self._logging.debug('Request status: %s', req)

                twins = list( map(lambda x: {
                    'urn': x,
                    'status': GlobalParamters.Status.NEW.name,
                    'shell': {},
                    'checkresult': [],
                    'bpn': bpn['value']}, req.json()))
                fH.write_pickle(pickle_path, twins)

            except exceptions.RequestException as exc:
                self._logging.error(exc)
                raise SystemExit() from exc

        self._logging.info('.' * 60)
        self._logging.info('Feching the twins')
        if len(twins) >= 1:
            for i in tqdm(range(len(twins))):
                if twins[i]['status'] == GlobalParamters.Status.NEW.name:
                    # self._logging.debug(f"get Twin from Registry: {twins[i]}")
                    self._logging.debug("get Twin from Registry: %s", twins[i])
                    twins[i]['shell'] = self.get_twin(twins[i])
                    twins[i]['status'] = GlobalParamters.Status.TWINLOADED.name
                    # twins[i]['bpn'] = bpn['value']
                    sleep(uniform(0, 0.2))

                if i % 50 == 0:
                    fH.write_pickle(pickle_path, twins)
        else:
            self._logging.warning(
                'for %s %s no Twins exists in the Digital Twin Registry', 
                bpn['company'],
                bpn['value'])

        fH.write_pickle(pickle_path, twins)
        self._logging.info('')
        twins = [twin.pop('bpn', None) for twin in twins]
        return twins
