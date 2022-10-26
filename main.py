#!/usr/bin/env python

"""A programm to check if a Digital Twin in the Registry is conform to Catena-X specifications.
"""

import os.path
import logging
import logging.config
import datetime
import pandas as pd
import global_parameters as GlobalParamters
from registry_handler import RegistryHandler
from twin_check import TwinCheck
import file_handler as fH
from keycloack_handler_memory import KeycloackHandler

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


# ✅ CRITICAL SOLVE GLOBALS ISSUE ==> initialize only once if inctance exists?
# ✅ Add functionality to force reload
# ✅ Refactor code into Classes and restructure programm
# ✅ Add functionality fo Multiple BPN's
# ✅ draw Statusbar
# ✅ Proxy settings variable
# ✅ Documentation
# ✅ Refactor getTwinsByBPN force reload strategy (a pickl per bpn => abstraction a lot easier)
# Maybe: Write tests for checks(dont know how yet)
# Maybe: get VANs
# TODO: Add more information to resultset to identify an object
# TODO: Wrapping config in a class
# TODO: refactor config file 
# TODO: Add check against the testdatafile
# TODO: manufactureId Logic is not tested correctly

SETTINGS_FILENAME = 'settings_pentest.yaml'

def write_twin_as_csv(twins, bpn_o):
    """this function writes the result in a human readable result to disk

    :param twins: list of twins
    :type twins: list
    :param bpn: bpn of the twins
    :type bpn: string
    """
    for i in twins:
        del i['shell']
    df_twins = pd.DataFrame.from_dict(twins)
    df_twins.to_csv(f"{conf['check_output_filename']}_{bpn_o['company']}_{bpn_o['value']}_{datetime.datetime.now().strftime('%y%m%d')}.csv",
                    index=False,
                    header=True)


if __name__ == '__main__':

    # setup logging
    _logging_conf = fH.read_yaml(os.path.join(
        GlobalParamters.ROOT_DIR, 'logging.yaml'))
    logging.config.dictConfig(_logging_conf)
    _logging = logging.getLogger(__name__)

    # Writ start message
    _logging.info('#'*60)
    _logging.info('               START WEB SCRAPER')
    _logging.info('#'*60)

    #Load application configuration
    conf = fH.read_yaml(os.path.join(
        GlobalParamters.ROOT_DIR, SETTINGS_FILENAME))
    GlobalParamters.set_conf(conf)
    _logging.info('-' * 60)
    _logging.info('Configuration:')

    for key, value in GlobalParamters.CONF.items():
        # _logging.info(f'   {key:23} {value}')
        _logging.info('  %23s %s', key, value)

    _logging.info('-' * 60)

    # Application Setup
    _logging.info('Application Setup:')

    if GlobalParamters.CONF['force_reload']:
        GlobalParamters.set_force_reload(True)
    # _logging.info(f'   forced_reload\t\t{GlobalParamters.FORCE_RELOAD}')
    _logging.info('   forced_reload\t\t%s',GlobalParamters.FORCE_RELOAD)

    if 'proxies' in GlobalParamters.CONF:
        if GlobalParamters.CONF['proxies'] != {}:
            GlobalParamters.set_use_proxy(True)
        # _logging.info(f'   use_proxy\t\t\t{GlobalParamters.USE_PROXY}')
    _logging.info('   use_proxy\t\t\t%s',GlobalParamters.USE_PROXY)

    if len(GlobalParamters.CONF['bpn']) > 1:
        GlobalParamters.set_multiple_bpns(True)
    # _logging.info(f'   multiple_bpns\t\t{GlobalParamters.MULTIPLE_BPNS}')
    _logging.info('   multiple_bpns\t\t%s',GlobalParamters.MULTIPLE_BPNS)
    _logging.info('-' * 60)

    # Application start
    kcH = KeycloackHandler()
    rH = RegistryHandler(kcH)

    for bpn in conf['bpn']:

        if GlobalParamters.FORCE_RELOAD is True:
            file_name = f"{GlobalParamters.CONF['twins_pickle_pre_name']}_{bpn['value']}.pickle"
            pickle_path = os.path.join(GlobalParamters.ROOT_DIR, file_name)
            fH.remove_file(pickle_path)

        shells = rH.get_twins_by_bpn(bpn)
        tC = TwinCheck()
        shells = tC.check_twins(shells)
        write_twin_as_csv(shells, bpn)
