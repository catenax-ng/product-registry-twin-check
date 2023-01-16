
from requests import get
from urllib.parse import urlparse
from tqdm import tqdm
import logging
import global_parameters as GlobalParameters

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

## Example Code
# try:
#     headers = {
#                     'x-api-key': '123456'
#                 }

#     # provider = 'http://beta-edc.westeurope.cloudapp.azure.com:8282'
#     # edc_provider_url = 'https://connector.cx-casestudy.edc.aws.bmw.cloud/BPNL0000000004WK' # BMW
#     edc_provider_url = 'http://catenax-beta-edc.westeurope.cloudapp.azure.com:8282'
#     url = f'https://irs-consumer-controlplane.beta.demo.catena-x.net/data/catalog?providerUrl={edc_provider_url}/api/v1/ids/data'
    
#     req = requests.get(url,headers=headers)
    
#     print(req.status_code)
#     print(type(req.status_code))
#     if req.status_code == 200:
#         print('success')
    
#     if req.status_code == 500:
#         print(req.content)
    
#     # print(json.dumps(req.json(), indent=4))

# except Exception as e: 
#     print(e)
            
    
    
    
    
class EDCCheck ():
    """Class for all EDC Connector Check relevant topics
    """
    
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        pass
    
    def get_edc_endpoint_adresses(self,shells):
        endpointAddresses = []
        res = []
        for i in shells: 
            submodelDescriptors = i['shell']['submodelDescriptors']
            for submodelDescriptor in submodelDescriptors: 
                endpoints = submodelDescriptor['endpoints']
                
                for endpoint in endpoints: 
                    endpointAddress = endpoint['protocolInformation']['endpointAddress']
                    endpointAddress = endpointAddress.split('/urn:uuid')[0]
                    
                    if endpointAddress not in endpointAddresses:
                        endpointAddresses.append(endpointAddress) 
                        res.append(self._edc_check_obj(endpointAddress))
                        # print(endpointAddress)
                        self._logger.debug(endpointAddress)
                    
        return res
    
    def _edc_check_obj(self,url,response_conde='', err_msg=''):
        
        return {
            'url' : url,
            'response_code' : response_conde,
            'content' : err_msg
        }
        
    def check_all_edc_catalog_connectivity(self,shells):
        res = []
        addresses = self.get_edc_endpoint_adresses(shells)
        for i in tqdm(range(len(addresses))):
            res.append(self.get_edc_catalog(addresses[i]))
        return res

    def get_edc_catalog(self,edc_check_object):    
        try:
            headers = {'x-api-key': '123456'}
            
            url = f"{GlobalParameters.CONF['edc_consumer_control_plane']}/data/catalog?providerUrl={edc_check_object['url']}/api/v1/ids/data"    
                        
            if GlobalParameters.USE_PROXY is True:
                req = get(url, headers=headers,
                          proxies=GlobalParameters.CONF['proxies'])
            else:
                req = get(url, headers=headers)
            
            edc_check_object['response_code'] = req.status_code
            # if req.status_code != 200: 
            #     edc_check_object['content'] = req.content
            return edc_check_object

        except Exception as e: 
            print(e)
        pass