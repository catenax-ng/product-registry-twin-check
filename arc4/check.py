from asyncore import loop
import os
import logging
import logging.config
import yaml
import requests
from urllib.parse import urljoin
import datetime
from time import sleep
import random
import re
from pprint import pprint
from enum import Enum
import pickle

# ✅ Write all 50 entries
# ✅ dev a timer with randomizer
# ✅ dev checks
#       - ✅ globalAssetId != aasId
#       - ✅ correct urn format
#       - ✅ correct semanticId 
#       - ✅ 'specificAssetIds': [{'key': 'ManufacturerId', 'value': 'BPNL00000003AYRE'} Check if ManufacturerId exists
# TODO: Proxy settings variable
# TODO: Exception handling
# TODO: Add functionality to force reload
# TODO: Refactor code into Classes and restructure programm
# TODO: Add file arg. for input
# TODO: Add configuration check
# TODO: Write tests (hard, dont know how yet)
# TODO: Clean up registry Handler



# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Check(Enum):
    PASSED = 1
    FAILED = 2    

class Status(Enum):
    NEW = 1
    TWINLOADED = 2
    TESTED = 3

# def read_yaml(file_path):
#     """returns the yaml contents

#     :param file_path: path of the yaml file
#     :type file_path: string
#     :return: dictionary with yaml content
#     :rtype: dict
#     """
#     try:
#         with open(file_path, "r") as f:
#             return yaml.safe_load(f)
#     except EnvironmentError as e:
#         #logger.error(e)
#         raise EnvironmentError()



# def get_token():

#     KEYCLOAK_HOST_FULL = f"{conf['keycloack_host']}{conf['keycloack_realm']}"
#     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#     data = {
#         'grant_type': 'client_credentials',
#         'client_id': conf['client_id'],
#         'client_secret': conf['client_secret']
#     }

#     # check if pickl exists
#     token_pickle = os.path.join(ROOT_DIR, conf['token_pickle'])
#     get_token = False
#     token = {}
#     token['access_token_expiry'] = datetime.datetime.now() + \
#         datetime.timedelta(seconds=-100)

#     if os.path.isfile(token_pickle):
#         token = pickle.load(open(token_pickle, 'rb'))
#     else:
#         get_token = True

#     if token['access_token_expiry'] <= datetime.datetime.now():
#         get_token = True

#     if get_token:
#         logging.info('REFRESH TICKET')
#         req = requests.post(KEYCLOAK_HOST_FULL, data=data, headers=headers)
#         token = req.json()
#         token['access_token_expiry'] = datetime.datetime.now(
#         ) + datetime.timedelta(seconds=token['expires_in'])
        
#         pickle.dump(token, open(token_pickle, 'wb'))

#         # logging.info(f"Token expires at {token['access_token_expiry']}")
#     return token['access_token']

# def getTwin(aasId):
#     try:
#         # aasIdentifier = 'urn:uuid:1c7dfb85-53de-42cf-bc07-fe702916ffb8'
#         getShell= f"registry/registry/shell-descriptors/{aasId['urn']}"
#         url = urljoin(conf['registry_url'],getShell)
#         # logger.debug(f'url: {url}')
#         headers ={
#             'Authorization':f'Bearer {get_token()}'
#         }

#         req = requests.get(url,headers=headers, proxies=conf['proxies'])
#         # logger.debug(f'Request status: {req}')
#         # logger.debug(req.json())
        
#     except requests.exceptions.RequestException as e:
#         logger.error(e)
#         raise SystemExit()
#     return req.json()



# def getShellsByBPN(bpn):
#     logging.info(f'Getting all aasIds for BPN: {bpn}')
     
#     twins_pickle = os.path.join(ROOT_DIR, conf['twins_pickl_filename'])
    
#     twins = []
#     loadtwins = False
    
#     if os.path.isfile(twins_pickle):
#         twins = pickle.load(open(twins_pickle, 'rb'))
#     else:
#         loadtwins = True
    
#     if loadtwins: 
#         try:
#             params = """assetIds=[{"key":"ManufacturerId","value":\""""+bpn['value']+""""}]"""
#             get_shells = f"registry/lookup/shells"
#             url = urljoin(conf['registry_url'], get_shells)
#             logger.debug(f'url: {url}')
#             headers = {
#                 'Authorization': f'Bearer {get_token()}',
#                 'Content-Type': 'application/x-www-form-urlencoded'

#             }
#             req = requests.get(url, params=params, headers=headers)
#             logger.debug(f'Request status: {req}')
            
#             twins = list(map( lambda x : { 'urn':x, 'status':Status.NEW.name,'shell':{}, 'checkresult':[]},req.json()))
#             pickle.dump( twins, open(twins_pickle,'wb'))
            
#         except requests.exceptions.RequestException as e:
#             logger.error(e)
#             raise SystemExit()
        

#     numAasId= len(twins)
#     logging.info(f' {numAasId} aasIds have been fetched')
    
#     logging.info(' Feching the twins')
    
#     for i in range(len(twins)):
#     # for i in range(0,10):      
#         if twins[i]['shell'] == {} or twins[i]['status'] == Status.NEW.name:
#             twins[i]['shell']= getTwin(twins[i])
#             twins[i]['status'] = Status.TWINLOADED.name
#             logger.debug(f"uuid: {twins[i]['urn']}")
#             sleep(random.uniform(0,0.5))
        
#         if i % 100 == 0:
#             pickle.dump( twins, open(twins_pickle,'wb'))
#             logging.info(f'twins safed: {i}')
        
#     pickle.dump( twins, open(twins_pickle,'wb'))

    
#     return twins    

# def twinCheck(twins):
    
#     logging.info('Start Twin Checkup')
    
#     for i in range(len(twins)):
#         twins[i]['checkresult'].append(check1(twins[i]))
#         twins[i]['checkresult'].append(check2(twins[i]))
#         twins[i]['checkresult'].append(check3(twins[i]))
#         twins[i]['checkresult'].append(check4(twins[i]))

#         # Set Check if all tests have passed
#         twins[i]['check'] = Check.FAILED.name        
#         if len([x for x in twins[i]['checkresult'] if x['result'] == Check.FAILED.name]) == 0:
#             twins[i]['check'] = Check.PASSED.name
        
#         # set Status
#         twins[i]['status'] = 'tested'
        
#     twins_pickle = os.path.join(ROOT_DIR, conf['twins_pickl_filename'])
#     pickle.dump( twins, open(twins_pickle,'wb'))
    
    

# def check1(twin):
    
#     check1 = { 'id':'check1', 'name':'globalAssetId != aasId validation'}
#     shell = twin['shell']
    
#     if shell['globalAssetId']['value'][0] != shell['identification']:
#         check1['result'] = Check.PASSED.name
#     else:
#         check1['result'] = Check.FAILED.name
    
#     return check1

# def check2(twin):
    
#     check2 = { 'id':'check2', 'name':'Check if correct SemanticID exists'}
#     shell = twin['shell']
    
#     semanticIDs = [
#         'urn:bamm:io.catenax.serial_part_typization:1.1.0#SerialPartTypization',
#         'urn:bamm:io.catenax.assembly_part_relationship:1.1.0#AssemblyPartRelationship',
#         'urn:bamm:io.catenax.material_for_recycling:1.1.0#MaterialForRecycling',
#         'urn:bamm:io.catenax.certificate_of_destruction:1.0.0#CertificateOfDestruction',
#         'urn:bamm:io.catenax.vehicle.product_description:1.0.1#ProductDescription',
#         'urn:bamm:io.catenax.battery.product_description:1.0.1#ProductDescription',
#         'urn:bamm:io.catenax.return_request:1.0.0#ReturnRequest',
#         'urn:bamm:io.catenax.physical_dimension:1.0.0#PhysicalDimension',
#         'urn:bamm:io.catenax.batch:1.0.0#Batch'
#     ]
    
#     # urn:bamm:io.catenax.vehicle.product_description:1.0.0#ProductDescription
#     # urn:bamm:io.catenax.vehicle.product_description:1.0.1#ProductDescription
    
#     check2['result'] = Check.PASSED.name
#     check2['info'] = []

    
#     for i in range(len(shell['submodelDescriptors'])):
#         id = shell['submodelDescriptors'][i]['semanticId']['value'][0]      
#         if id not in semanticIDs:
#             check2['result'] = Check.FAILED.name
#             check2['info'].append(f"format is wrong: {id}")

#     return check2

# def check3(twin):

#     check3 = { 'id':'check3', 'name':'Check if ManufacturerId exists in specificAssetIds'}
#     shell = twin['shell']
#     check = [x for x in shell['specificAssetIds'] if x['key'] == 'ManufacturerId']
#     if not check:
#         check3['result'] = Check.FAILED.name
#     else: 
#         check3['result'] = Check.PASSED.name
#     return check3


# def check4(twin):
    
#     check4 = { 'id':'check4', 'name':'Check if aasID has valid urn uuid format'}
#     shell = twin['shell']
    
#     comp = re.compile("urn:uuid:[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}")
    
#     if comp.match(shell['identification']):
#         check4['result'] = Check.PASSED.name
    
#     return check4


def extractResult(twins):
    
    import pandas as pd
    for i in twins:
        del i['shell']
    df = pd.DataFrame.from_dict(twins) 
    df.to_csv(f"{conf['check_output_filename']}.csv", index = False, header=True)
    

if __name__ == '__main__':

    # get directory of this file
    # load YAML logging file
    logger_conf = read_yaml(os.path.join(ROOT_DIR, 'logging.yaml'))

    # setup logging
    logging.config.dictConfig(logger_conf)
    logger = logging.getLogger(__name__)

    logger.info('#'*60)
    logger.info('               START WEB SCRAPER')
    logger.info('#'*60)

    conf = read_yaml(os.path.join(ROOT_DIR, 'settings.yaml'))
    # logger.debug(conf)
    
    TWINS_PICKL_PATH = os.path.join(ROOT_DIR, conf['twins_pickl_filename'])

    
    shells = getShellsByBPN(conf['bpn'][0])
    

    
    extractResult(shells)