""" Global Parameters for this programm
"""

import os.path
from enum import Enum

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

ROOT_DIR= os.path.dirname(os.path.abspath(__file__))
CONF = {}
LOGGER_CONF = {}
FORCE_RELOAD:bool = False
USE_PROXY:bool = False
MULTIPLE_BPNS:bool = False

class Status(Enum):
    """ Class for all enum values which are the states a twin can reach
    """
    NEW = 1
    TWINLOADED = 2
    TESTED = 3

def set_conf(conf):
    """ set configuration
    :param conf: configuration
    :type conf: dict
    """
    global CONF
    CONF = conf

def set_force_reload(is_force_reload:bool):
    """ set force reload
    :param is_force_reload: is force reload enabled
    :type is_force_reload: bool
    """
    global FORCE_RELOAD
    FORCE_RELOAD = is_force_reload

def set_use_proxy(use_proxy:bool):
    """set use proxy

    :param use_proxy: is proxy in use
    :type use_proxy: bool
    """
    global USE_PROXY
    USE_PROXY = use_proxy

def set_multiple_bpns(is_multiple_bpns:bool):
    """set multiple bpns

    :param is_multiple_bpns: _description_
    :type is_multiple_bpns: bool
    """
    global MULTIPLE_BPNS
    MULTIPLE_BPNS = is_multiple_bpns

def set_logger_conf(conf):
    """ set logger configuration

    :param conf: _description_
    :type conf: _type_
    """
    global LOGGER_CONF
    LOGGER_CONF = conf