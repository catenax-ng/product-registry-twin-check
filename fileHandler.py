
from os import walk
import os
import errno
import logging
import logging.config
import pickle
import string
import yaml
import globalParamters


class fileHandler:
    """Class to handle all communication with writing and reading the disk
    """
    def __init__(self ) -> None:
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
        self.logging.debug(f'file is beeing created: {filename}')
        with open(filename, mode) as f:
            f.write(content)

    
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
        self.logging.debug(f'file is beeing created: {file_path}')
        with open(file_path, mode=mode) as f:
            pickle.dump(content, f)
    
    
    def load_pickle(self,file_path:string,mode='rb'):
        """_summary_

        :param path: path to open
        :type path: string
        :param mode: _description_, defaults to 'rb'
        :type mode: str, optional
        """
        
        if os.path.exists(file_path):
            self.logging.debug(f'file exists: {file_path}')
            try:
                with open(file_path, mode=mode) as f: 
                    return pickle.load(f)
            except EnvironmentError:
                raise EnvironmentError()
        else:
            self.logging.error(f'file does not exist: {file_path}')

    
    def read_yaml(self, file_path):
        """returns the yaml contents

        :param file_path: path of the yaml file
        :type file_path: string
        :return: dictionary with yaml content
        :rtype: dict
        """
        if '.yaml' in file_path:
            try:
                with open(file_path, "r") as f:
                    return yaml.safe_load(f)
            except EnvironmentError as e:
                self.logging.error(e)
                raise EnvironmentError()
        else:
            self.logging.error('file is not a .yaml file')
    
    def remove_file(self,file_path):
        """remove file if exists

        :param file_path: filepath
        :type file_path: string
        """
        if os.path.exists(file_path):
            try: 
                os.remove(file_path)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
        else:
            self.logging.error("Can not delete the file as it doesn't exists.")
    
    

_inst = fileHandler()
write = _inst.write
write_pickle = _inst.write_pickle
load_pickle = _inst.load_pickle
read_yaml = _inst.read_yaml
remove_file = _inst.remove_file