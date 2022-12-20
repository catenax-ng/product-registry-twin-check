
""" file handler to manage interaction with writing and reading files
"""
import os
import errno
import logging
import logging.config
import pickle
import string
import yaml

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

class FileHandler:
    """Class to handle all communication with writing and reading the disk
    """

    def __init__(self) -> None:
        self.logging = logging.getLogger(__name__)

    def write(self, filename, content, mode='wb'):
        """_summary_

        :param filename: _description_
        :type filename: _type_
        :param content: _description_
        :type content: _type_
        :param mode: _description_, defaults to 'wb'
        :type mode: str, optional
        """
        # path = os.path.join(globals.ROOT_DIR,filename)
        # if os.path.exists(path):
        #     logging.debug(f'file exists: {path}')
        #     pass
        # else:
        self.logging.debug('file is beeing created: %s', filename)

        with open(filename, mode, encoding='utf-8') as fio:
            fio.write(content)

    def write_pickle(self, file_path, content, mode='wb'):
        """_summary_

        :param path: path of file
        :type path: string
        :param content: object which is written to the pickle file
        :type content: any
        :param mode: mode in which pickle opens the file , defaults to 'wb'
        :type mode: str, optional
        """

        # if os.path.exists(file_path):
        #     self.logging.debug(f'file exists: {file_path}')
        #     pass
        # else:
        self.logging.debug('file is beeing created: %s', file_path)
        with open(file_path, mode=mode) as fio:
            pickle.dump(content, fio)

    def load_pickle(self, file_path: string, mode='rb'):
        """_summary_

        :param path: path to open
        :type path: string
        :param mode: _description_, defaults to 'rb'
        :type mode: str, optional
        """

        if os.path.exists(file_path):
            self.logging.debug('file exists: %s', file_path)
            try:
                with open(file_path, mode=mode) as fio:
                    return pickle.load(fio)
            except EnvironmentError as exc:
                raise EnvironmentError() from exc
        else:
            self.logging.error('file does not exist: %s',file_path)

    def read_yaml(self, file_path):
        """returns the yaml contents

        :param file_path: path of the yaml file
        :type file_path: string
        :return: dictionary with yaml content
        :rtype: dict
        """
        if '.yaml' in file_path:
            try:
                with open(file_path, "r", encoding='utf-8') as fio:
                    return yaml.safe_load(fio)
            except EnvironmentError as exc:
                self.logging.error(exc)
                raise EnvironmentError() from exc
        else:
            self.logging.error('file is not a .yaml file')
            return None

    def remove_file(self, file_path):
        """remove file if exists

        :param file_path: filepath
        :type file_path: string
        """
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as exc:
                if exc.errno != errno.ENOENT:
                    raise
        else:
            self.logging.error("Can not delete the file as it doesn't exists.")


_inst = FileHandler()
write = _inst.write
write_pickle = _inst.write_pickle
load_pickle = _inst.load_pickle
read_yaml = _inst.read_yaml
remove_file = _inst.remove_file
