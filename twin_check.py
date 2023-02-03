"""This Modul holds all Twin Check relvant classes, methods and tests
"""

import logging
from enum import Enum
import re
from tqdm import tqdm
import global_parameters as GlobalParamters
import file_handler as fH
import json

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
        self.prepared_data = self.prepare_test_data()
        self.unique_expected_bpns = self.get_unique_expected_bpns()
        self.unique_expected_gAIs = self.get_unique_expected_gAIs()
        self._seen_gAIs = set()
        self._duplicates_gAIs = []

    def check_twins(self, twins):
        """apply the checks to the twins

        :param twins: twins
        :type twins: list
        :return: twins with check result
        :rtype: list
        """
        self._logger.info('.'*60)
        self._logger.info('Start Twin Checkup')
        self._logger.info('is checking %d twins', len(twins))

        # prepare list of duplicate globalAssetIds
        for i in range(len(twins)):
            _, gAI = self.check_globalAssetId(twins[i])
            if gAI in self._seen_gAIs:
                self._duplicates_gAIs.append(gAI)
            else:
                self._seen_gAIs.add(gAI)

        for i in tqdm(range(len(twins))):
            if 'status' not in twins[i] or twins[i]['status'] == GlobalParamters.Status.TWINLOADED.name:

                twins[i]['aas uuid:urn format'] = self.check_aasId_valid_urn_format(
                    twins[i])
                twins[i]['globalAssetId exists'], twins[i]['globalAssetId'] = self.check_globalAssetId(
                    twins[i])
                twins[i]['globalAssetId uuid:urn format'] = self.check_globalAssetId_valid_urn_format(
                    twins[i])
                twins[i]['unique globalAssetId'] = self.check_globalAssetId_is_uniques(
                    twins[i])
                twins[i]['aasId!=globalAssetId'] = self.check_aasId_not_globalAssetId(
                    twins[i])

                twins[i]['valid semanticIds'], twins[i]['valid semanticIds info'] = self.check_valid_semanicIds(
                    twins[i])

                for ids in GlobalParamters.CONF['semanticIds']:
                    semantic_id = ids['semanticId']
                    if 'linkedSpecificAssetIds' in ids:
                        for linked_specific_assetId in ids['linkedSpecificAssetIds']:

                            specific_asset_id = linked_specific_assetId['specificAssetId']
                            check_level = linked_specific_assetId['checkLevel']

                            check_column_name = ''
                            check_info_column_name = ''
                            if check_level == 'optional':
                                check_column_name = f'optional {specific_asset_id} in specificAssetIds'
                                check_info_column_name = f'optional {specific_asset_id} in specificAssetIds info'
                                twins[i][check_column_name], twins[i][check_info_column_name] = self.check_optional_Id_in_specificAssetId(
                                    twins[i], specific_asset_id)

                            else:
                                check_column_name = f'{specific_asset_id} in specificAssetIds'
                                check_info_column_name = f'{specific_asset_id} in specificAssetIds info'
                                twins[i][check_column_name], twins[i][check_info_column_name] = self.check_Id_in_specificAssetId(
                                    twins[i], specific_asset_id)

                            if specific_asset_id == 'manufacturerId':
                                twins[i]['bpn'], twins[i]['bpn schema'] = self.extract_bpn(
                                    twins[i])

                # Check against Testdata
                # Check if bpn matches
                twins[i]['twin bpn matches to expected bpn'] = self.check_bpn_against_expected_bpn(
                    twins[i])
                # Check if globalAssetId is in expected globalAssetIds
                twins[i]['twin globalAssetId matches to expected globalAssetId'] = self.check_gAI_against_expected_gAI(
                    twins[i])

                twins[i]['check'] = Check.PASSED.name
                if Check.FAILED.name in twins[i].values():
                    twins[i]['check'] = Check.FAILED.name

                # set Status
                twins[i]['status'] = GlobalParamters.Status.TESTED.name

        self._logger.info(' ')
        return twins

    def check_aasId_valid_urn_format(self, twin):
        """Tis checks if an ID has a valid URN:UUID Format

        :param twin: digital twin
        :type twin: dict
        :return: test result 
        :rtype: string
        """
        result = Check.FAILED.name
        shell = twin['shell']
        comp = re.compile(
            "urn:uuid:[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}")

        if comp.match(shell['identification']):
            result = Check.PASSED.name
        else:
            result = Check.FAILED.name

        return result

    def check_globalAssetId(self, twin):
        """check if globalAssetId exists

        :param twin: digital twin
        :type twin: dict
        :return: check result 
        :rtype: string
        """
        result = Check.FAILED.name
        shell = twin['shell']
        globalAssetId = ''
        if 'globalAssetId' in shell:
            if 'value' in shell['globalAssetId']:
                if len(shell['globalAssetId']['value']) > 0:
                    result = Check.PASSED.name
                    globalAssetId = shell['globalAssetId']['value'][0]
        return result, globalAssetId

    def check_globalAssetId_is_uniques(self, twin):
        result = Check.FAILED.name
        shell = twin['shell']

        if shell['globalAssetId']['value'][0] not in self._duplicates_gAIs:
            result = Check.PASSED.name
        return result

    def check_globalAssetId_valid_urn_format(self, twin):
        """Tis checks if an ID has a valid URN:UUID Format

        :param twin: digital twin
        :type twin: dict
        :return: test result
        :rtype: string
        """
        result = Check.FAILED.name
        shell = twin['shell']
        comp = re.compile(
            "urn:uuid:[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}")
        if 'globalAssetId' in shell:
            if 'value' in shell['globalAssetId']:
                if len(shell['globalAssetId']['value']) > 0:
                    if comp.match(shell['globalAssetId']['value'][0]):
                        result = Check.PASSED.name

        return result

    def check_aasId_not_globalAssetId(self, twin):
        """This checks if the global AssetId is different to the aasID

        :param twin: digital twin
        :type twin: dict
        :return: test result 
        :rtype: string
        """
        result = Check.FAILED.name
        shell = twin['shell']
        if 'globalAssetId' in shell:
            if shell['globalAssetId']['value'][0] != shell['identification']:
                result = Check.PASSED.name
            else:
                result = Check.FAILED.name
        else:
            result = Check.FAILED.name
        return result

    def check_valid_semanicIds(self, twin):
        """check2 checks if the semanticIDs are of a valid structure

        :param twin: digital twin
        :type twin: dict
        :return: tuple check result, info
        :rtype: tuple(string, arr)
        """
        result = Check.PASSED.name
        shell = twin['shell']

        semantic_ids = list(
            map(lambda x: x['semanticId'], GlobalParamters.CONF['semanticIds']))

        info = []

        for i in range(len(shell['submodelDescriptors'])):
            semantic_id = shell['submodelDescriptors'][i]['semanticId']['value'][0]
            if semantic_id not in semantic_ids:
                result = Check.FAILED.name
                info.append(semantic_id)
        return result, info

    def extract_bpn(self, twin):
        """check if BPN exists and validates against the BPN Schema

        :param twin: digital twin
        :type twin: dict
        :return: bpn, schema check result
        :rtype: tuple (string,string)
        """
        bpn = ''
        valid_key = 'manufacturerId'
        shell = twin['shell']
        result = ''
        valid_key_found = [x for x in shell['specificAssetIds']
                           if x['key'].lower() == valid_key.lower()]
        comp = re.compile("BPN[0-9A-Z]{12}")

        if len(valid_key_found) > 0:
            bpn = valid_key_found[0]['value']

            if comp.match(bpn):
                result = Check.PASSED.name
            else:
                result = Check.FAILED.name

        return bpn, result

    def check_Id_in_specificAssetId(self, twin, id):
        """This checks if a ID exists in specificAssetIds and is written correctly with camel case

        :param twin: digital twin
        :type twin: dict
        :return: tuple check result, info
        :rtype: tuple(string, arr)
        """

        valid_key = id
        result = Check.FAILED.name
        info = ''
        shell = twin['shell']

        valid_key_found = [x for x in shell['specificAssetIds']
                           if x['key'].lower() == valid_key.lower()]
        valid_key_correct = [x for x in shell['specificAssetIds'] if x['key'].lower(
        ) == valid_key.lower() and x['key'] == valid_key]

        if len(valid_key_found) > 0 and len(valid_key_correct) > 0:
            result = Check.PASSED.name
            info = valid_key_correct[0]
        elif len(valid_key_found) > 0 and len(valid_key_correct) < 1:
            info = f"{id} does not fit to expected format current: {valid_key_found[0]}"
        elif len(valid_key_found) < 1:
            info = f"{id} not found"

        return result, str(info)

    def check_optional_Id_in_specificAssetId(self, twin, id):
        """This checks if a ID exists in specificAssetIds and is written correctly with camel case

        :param twin: digital twin
        :type twin: dict
        :return: tuple check result, info
        :rtype: tuple(string, string)
        """

        valid_key = id
        result = ''
        info = ''
        shell = twin['shell']

        valid_key_found = [x for x in shell['specificAssetIds']
                           if x['key'].lower() == valid_key.lower()]
        valid_key_correct = [x for x in shell['specificAssetIds'] if x['key'].lower(
        ) == valid_key.lower() and x['key'] == valid_key]

        if len(valid_key_found) > 0 and len(valid_key_correct) > 0:
            result = Check.PASSED.name
        elif len(valid_key_found) > 0 and len(valid_key_correct) < 1:
            info = f"key does not fit to expected format: {id}"
            result = Check.FAILED.name
        elif len(valid_key_found) < 1:
            info = ''
            result = ''

        return result, info

    def check_bpn_against_expected_bpn(self, twin):
        """This check the bpn against a bpn from the test data files

        :param twin: digital twin
        :type twin: dict
        :return: check result
        :rtype: string
        """
        result = Check.FAILED.name
        if twin['bpn'] in self.unique_expected_bpns:
           result = Check.PASSED.name
        return result

    def check_gAI_against_expected_gAI(self, twin):
        """This checks the globalAssetId against the globalAssetIds provided in the test data files

        :param twin: digital twin
        :type twin: dict
        :return: check result
        :rtype: string
        """
        result = Check.FAILED.name
        shell = twin['shell']

        if shell['globalAssetId']['value'][0] in self.unique_expected_gAIs:
           result = Check.PASSED.name
        return result

    def prepare_test_data(self):
        """prepares the test data

        :return: list of all twins within the test data files
        :rtype: list
        """
        expected_twins = []

        file_paths = fH.get_test_files()
        for file_path in file_paths:
            # TODO: get the correct Object with config of testdatafile
            expected_twins.extend(fH.read_structured_file(file_path)[
                                  'https://catenax.io/schema/TestDataContainer/1.0.0'])
        return expected_twins

    def get_unique_expected_bpns(self):
        return list(set(map(lambda ent: ent['bpnl'], self.prepared_data)))

    def get_unique_expected_gAIs(self):
        return list(set(map(lambda ent: ent['catenaXId'], self.prepared_data)))
