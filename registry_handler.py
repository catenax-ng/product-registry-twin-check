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

    def _globalAssetId(self,twin):
        res = None
        if 'globalAssetId' in twin:
            if 'value' in twin['globalAssetId']:
                if len(twin['globalAssetId']['value']) > 0:
                    res = twin['globalAssetId']['value'][0]
                else:
                    res = twin['globalAssetId']['value']
            else:
                res = twin['globalAssetId']
        else:
            res = f"\"[{twin}]\""  
                            
        return res

    def _transform_items(self,x):
        res =  list(map(lambda x: {
                    'aasId':  x['identification'],
                    'status': GlobalParamters.Status.TWINLOADED.name,
                    'shell': x,
                    },x))
        return res
        
        # globalAssetId": {
        #         "value": [
        #             "urn:uuid:0ece43f1-7bd0-11e1-b359-ecad00e4333"
        #         ]
        #     },

    def get_twin(self, aas_id):
        """Retrieves a twin for a specific aasId

        :param aasId: Asset Administration Id from a
        :type aasId: string
        :return: twin
        :rtype: dict
        """
        try:
            get_shell = f"registry/registry/shell-descriptors/{aas_id['aasId']}"
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
            self._logging.debug('Request status: %s', req)
            self._logging.debug('Request payload: %s', req.json())

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

        self._logging.info('Getting all Twins for BPN: %s', bpn)
        twins = []
        load_twin_list = False
        file_name = f"{GlobalParamters.CONF['twins_pickle_pre_name']}_{bpn['value']}.pickle"
        pickle_path = os.path.join(GlobalParamters.ROOT_DIR, file_name)
        manufacturerId = 'manufacturerId'
        if os.path.isfile(pickle_path):
            twins = fH.load_pickle(pickle_path, 'rb')
            self._logging.info(' Twins loaded from file.')

            # len([twin for twin in twins if twin['bpn'] == bpn['value'] ])
            # if len([twin for twin in twins if twin['bpn'] == bpn['value'] ]) == 0:
            #     self._logging.info('No values found for %s', bpn['value'] )
            #     load_twin_list = True
            # else:
            #     return [twin for twin in twins if twin['bpn'] == bpn['value'] ]
        else:
            load_twin_list = True

        self._logging.info(
            "load_twin_list: %s, pikle path: %s", load_twin_list, pickle_path)

        if load_twin_list:
            self._logging.info(' Fetch twins from registry.')
            try:
                params = """assetIds=[{"key":\"""" + manufacturerId + """","value":\"""" + \
                    bpn['value']+""""}]"""
                get_shells = "registry/lookup/shells"
                url = urljoin(GlobalParamters.CONF['registry_url'], get_shells)
                self._logging.debug('url: %s', url)
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

                twins = list(map(lambda x: {
                    'aasId': x,
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
                'for %s %s no Twins exists in the Digital Twin Registry. Check if %s is in the correct format',
                bpn['company'],
                bpn['value'], manufacturerId)

        fH.write_pickle(pickle_path, twins)
        self._logging.info('')
        self._logging.info('safed %d twins to file', len(twins))
        self._logging.info('')
        self._logging.info('')

        # twins = [twin.pop('bpn', None) for twin in twins]
        return twins

    def _getPage(self,page=0,pageSize=20):
        get_shells = f"/registry/registry/shell-descriptors/?page={page}&pageSize={pageSize}"
        url = urljoin(GlobalParamters.CONF['registry_url'], get_shells)
        self._logging.debug('url: %s', url)
        headers = {
            'Authorization': f'Bearer {self.kc_h.get_token()}',
            'Content-Type': 'application/x-www-form-urlencoded'

            }

        if GlobalParamters.USE_PROXY is True:
            req = get(url, headers=headers,
                        proxies=GlobalParamters.CONF['proxies'])
        else:
            req = get(url,
                        headers=headers, proxies=None)

        self._logging.debug('Request status: %s', req)
        
        return req

    def get_all_twins(self):
        self._logging.info('Getting all Twins')
        twins = []
        load_twin_list = False

        file_name = f"all_twins.pickle"
        pickle_path = os.path.join(GlobalParamters.ROOT_DIR, file_name)
        
        if os.path.isfile(pickle_path):
            twins = fH.load_pickle(pickle_path, 'rb')
            self._logging.info(' Twins loaded from file.')
        else:
            load_twin_list = True

        if load_twin_list:
            self._logging.info(' Fetch twins from registry.')
            try:
                req = self._getPage().json()
                twins = self._transform_items(req['items'])

                for i in tqdm(range(1, req['totalPages'])):
                    page = self._getPage(i).json()
                    twins.extend(self._transform_items(page['items']))

                fH.write_pickle(pickle_path, twins)

            except exceptions.RequestException as exc:
                self._logging.error(exc)
                raise SystemExit() from exc

        return twins
