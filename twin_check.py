"""This Modul holds all Twin Check relvant classes, methods and tests
"""

import logging
from enum import Enum
import re
from tqdm import tqdm
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
    """Class for an Check Enumerations for passing or failing a check.
    """
    PASSED = 1
    FAILED = 2


class TwinCheck:
    """class for the different checks.

    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def check_twins(self,twins):
        """apply the checks to the twins

        :param twins: twins
        :type twins: list
        :return: twins with check result
        :rtype: list
        """
        self._logger.info('.'*60)
        self._logger.info('Start Twin Checkup')
        self._logger.debug('is checking %d twins', len(twins))
        for i in tqdm(range(len(twins))):
            if 'status' not in twins[i] or twins[i]['status'] == GlobalParamters.Status.TWINLOADED.name:
                twins[i]['checkresult'].append(self.check1(twins[i]))
                twins[i]['checkresult'].append(self.check2(twins[i]))
                twins[i]['checkresult'].append(self.check3(twins[i]))
                twins[i]['checkresult'].append(self.check4(twins[i]))
                twins[i]['checkresult'].append(self.check5(twins[i]))
                twins[i]['checkresult'].append(self.check6(twins[i]))
                twins[i]['checkresult'].append(self.check7(twins[i]))
                twins[i]['checkresult'].append(self.check8(twins[i]))

                # Set Check if all tests have passed
                twins[i]['check'] = Check.FAILED.name
                if len([x for x in twins[i]['checkresult']
                        if x['result'] == Check.FAILED.name]) == 0:
                    twins[i]['check'] = Check.PASSED.name

                # set Status
                twins[i]['status'] = GlobalParamters.Status.TESTED.name
        self._logger.info(' ')
        return twins

    def check1(self,twin):
        """This checks if the global AssetId is different to the aasID

        :param twin: digital twin
        :type twin: dict
        :return: test result object
        :rtype: dict
        """
        check1 = { 'id':'check1', 'name':'globalAssetId != aasId validation'}
        shell = twin['shell']

        if shell['globalAssetId']['value'][0] != shell['identification']:
            check1['result'] = Check.PASSED.name
        else:
            check1['result'] = Check.FAILED.name

        return check1



    def check2(self,twin):
        """check2 checks if the semanticIDs are of a valid structure

        :param twin: digital twin
        :type twin: dict
        :return: test result object
        :rtype: dict
        """

        check2 = { 'id':'check2', 'name':'Check if correct SemanticID exists'}
        shell = twin['shell']

        semantic_ids = [
            'urn:bamm:io.catenax.serial_part_typization:1.1.0#SerialPartTypization',
            'urn:bamm:io.catenax.assembly_part_relationship:1.1.0#AssemblyPartRelationship',
            'urn:bamm:io.catenax.material_for_recycling:1.1.0#MaterialForRecycling',
            'urn:bamm:io.catenax.certificate_of_destruction:1.0.0#CertificateOfDestruction',
            'urn:bamm:io.catenax.vehicle.product_description:1.0.1#ProductDescription',
            'urn:bamm:io.catenax.battery.product_description:1.0.1#ProductDescription',
            'urn:bamm:io.catenax.return_request:1.0.0#ReturnRequest',
            'urn:bamm:io.catenax.physical_dimension:1.0.0#PhysicalDimension',
            'urn:bamm:io.catenax.batch:1.0.0#Batch'
        ]

        check2['result'] = Check.PASSED.name
        check2['info'] = []

        for i in range(len(shell['submodelDescriptors'])):
            semantic_id = shell['submodelDescriptors'][i]['semanticId']['value'][0]
            if semantic_id not in semantic_ids:
                check2['result'] = Check.FAILED.name
                check2['info'].append(f"format is wrong: {semantic_id}")

        return check2



    def check3(self,twin):
        """This checks if a manaufacturerId is specified in the specificAssetIds

        :param twin: digital twin
        :type twin: dict
        :return: test result object
        :rtype: dict
        """
        valid_key = 'manufacturerId'
        check3 = { 'id':'check3', 'name':f'Check if {valid_key} exists in specificAssetIds'}
        shell = twin['shell']
        check = [x for x in shell['specificAssetIds'] if x['key'] == valid_key]
        if not check:
            check3['result'] = Check.FAILED.name
        else:
            check3['result'] = Check.PASSED.name
        return check3


    def check4(self,twin):
        """Tis checks if an ID has a valid URN:UUID Format

        :param twin: digital twin
        :type twin: dict
        :return: test result object
        :rtype: dict
        """
        check4 = { 'id':'check4', 'name':'Check if aasID has valid urn uuid format'}
        shell = twin['shell']
        comp = re.compile("urn:uuid:[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}")

        if comp.match(shell['identification']):
            check4['result'] = Check.PASSED.name
        else: 
            check4['result'] = Check.FAILED.name

        return check4


    def check5(self,twin):
        """Tis checks if the shell contains key "van" in correct camelcase spelling in the specificAssetIds

        :param twin: digital twin
        :type twin: dict
        :return: test result object
        :rtype: dict
        """
        check5 = { 'id':'check5', 'name':'Check if the shell contains key "van" in correct camelcase spelling in the specificAssetIds'}
        shell = twin['shell']

        check5['result'] = Check.PASSED.name
        for entry in shell['specificAssetIds']:
            if entry['key'].lower() == 'van':
                if entry['key'] != 'van':
                    check5['result'] = Check.FAILED.name

        return check5


    def check6(self,twin):
        """This checks if a partInstanceId exists in specificAssetIds and is written correctly with camel case

        :param twin: digital twin
        :type twin: dict
        :return: test result object
        :rtype: dict
        """

        valid_key = 'partInstanceId'
        check = { 'id':'check6', 'name':f'Check if {valid_key} exists in specificAssetIds and is written correctly with camel case'}
        shell = twin['shell']
        
        valid_key_found = len([x for x in shell['specificAssetIds'] if x['key'].lower() == valid_key.lower()]) > 0
        valid_key_correct = len([x for x in shell['specificAssetIds'] if x['key'].lower() == valid_key.lower() and x['key'] == valid_key]) > 0

        if valid_key_found and valid_key_correct:
            check['result'] = Check.PASSED.name
        else:
            check['result'] = Check.FAILED.name

        return check


    def check7(self,twin):
        """This checks if mandatory attribute manufacturerPartId exists in specificAssetIds and is written correctly with camel case

        :param twin: digital twin
        :type twin: dict
        :return: test result object
        :rtype: dict
        """

        valid_key = 'manufacturerPartId'
        check = { 'id':'check7', 'name':f'Check if mandatory attribute {valid_key} exists in specificAssetIds and is written correctly with camel case'}
        shell = twin['shell']
        
        valid_key_found = len([x for x in shell['specificAssetIds'] if x['key'].lower() == valid_key.lower()]) > 0
        valid_key_correct = len([x for x in shell['specificAssetIds'] if x['key'].lower() == valid_key.lower() and x['key'] == valid_key]) > 0

        if valid_key_found and valid_key_correct:
            check['result'] = Check.PASSED.name
        else:
            check['result'] = Check.FAILED.name

        return check


    def check8(self,twin):
        """This checks if (optional) attribute customerPartId in specificAssetIds is written correctly with camel case

        :param twin: digital twin
        :type twin: dict
        :return: test result object
        :rtype: dict
        """

        valid_key = 'customerPartId'
        check = { 'id':'check8', 'name':f'Check if (optional) attribute {valid_key} in specificAssetIds is written correctly with camel case'}
        shell = twin['shell']
        
        valid_key_found = len([x for x in shell['specificAssetIds'] if x['key'].lower() == valid_key.lower()]) > 0
        valid_key_correct = len([x for x in shell['specificAssetIds'] if x['key'].lower() == valid_key.lower() and x['key'] == valid_key]) > 0

        if not valid_key_found or (valid_key_found and valid_key_correct):
            check['result'] = Check.PASSED.name
        else:
            check['result'] = Check.FAILED.name

        return check