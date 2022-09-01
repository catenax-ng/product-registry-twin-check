""" The Registry Handler manages all the communication with the Digital Twin Registry.
"""
from urllib.parse import urljoin
import fileHandler as fH
from requests import get, exceptions
import logging
import os
from enum import Enum
from time import sleep
from random import uniform
from tqdm import tqdm
import globalParamters

__author__ = "Johannes Zahn"
__copyright__ = """
 Copyright (c) 2022 
       2022: Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
 Copyright (c) 2022 Contributors to the Eclipse Foundation

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
    PASSED = 1
    FAILED = 2

class registryHandler:
    """Class to Handle the communication with the registry
    """

    def __init__(self, kcH) -> None:
        self._logging = logging.getLogger(__name__)
        self.kcH = kcH

    def getTwin(self,aasId):
        """Retrieves a twin for a specific aasId

        :param aasId: Asset Administration Id from a 
        :type aasId: string
        :return: twin
        :rtype: dict
        """
        try:
            getShell= f"registry/registry/shell-descriptors/{aasId['urn']}"
            url = urljoin(globalParamters.CONF['registry_url'],getShell)
            self._logging.debug(f'url: {url}')   
            headers ={
                'Authorization':f'Bearer {self.kcH.get_token()}'
            }
            
            if globalParamters.USE_PROXY == True:
                req = get(url,headers=headers, proxies=globalParamters.CONF['proxies'])
            else:
                req = get(url,headers=headers)

            self._logging.debug(f'Request status: {req}')
            self._logging.debug(f'Request payload: {req.json()}')
            
        except exceptions.RequestException as e:
            self._logging.error(e)
            raise SystemExit()
        
        return req.json()



    def getTwinsByBPN(self,bpn):
        """Retrieves al twins for a specific bpn

        :param bpn: Business Partner Number
        :type bpn: string
        :return: twins
        :rtype: list
        """
        
        self._logging.info(f'Getting all Twins for BPN: {bpn}')
        twins = []
        load_twin_list = False
        file_name = f"{globalParamters.CONF['twins_pickle_pre_name']}_{bpn['value']}.pickle"
        pickle_path = os.path.join(globalParamters.ROOT_DIR,file_name)

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
                    
        self._logging.info(f"load_twin_list: {load_twin_list}, pikle path: {pickle_path}")
        
        if load_twin_list: 
            try:
                params = """assetIds=[{"key":"ManufacturerId","value":\""""+bpn['value']+""""}]"""
                get_shells = f"registry/lookup/shells"
                url = urljoin(globalParamters.CONF['registry_url'], get_shells)
                self._logging.debug(f'url: {url}')
                headers = {
                    'Authorization': f'Bearer {self.kcH.get_token()}',
                    'Content-Type': 'application/x-www-form-urlencoded'

                }
                if globalParamters.USE_PROXY == True :
                    req = get(url, params=params, headers=headers, proxies=globalParamters.CONF['proxies'])
                else: 
                    req = get(url, params=params, headers=headers, proxies=None)
                
                self._logging.debug(f'Request status: {req}')
                
                twins = list(map( lambda x : { 'urn':x, 'status':globalParamters.Status.NEW.name,'shell':{}, 'checkresult':[], 'bpn':bpn['value']},req.json()))
                fH.write_pickle(pickle_path,twins)
                
            except exceptions.RequestException as e:
                self._logging.error(e)
                raise SystemExit()

        
        
        self._logging.info('.' *60)
        self._logging.info('Feching the twins')
        if len(twins) >= 1:
            for i in tqdm(range(len(twins))):
                if twins[i]['status'] == globalParamters.Status.NEW.name:
                    self._logging.debug(f"get Twin from Registry: {twins[i]}")
                    twins[i]['shell']= self.getTwin(twins[i])
                    twins[i]['status'] = globalParamters.Status.TWINLOADED.name
                    # twins[i]['bpn'] = bpn['value']
                    sleep(uniform(0,0.2))

                if i % 50 == 0:
                    fH.write_pickle(pickle_path,twins)
        else: 
            self._logging.warn('for %s %s no Twins exists in the Digital Twin Registry',bpn['company'], bpn['value'])

        fH.write_pickle(pickle_path,twins)
        self._logging.info('')
        [twin.pop('bpn', None) for twin in twins]
        return twins    