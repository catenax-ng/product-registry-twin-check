import os.path
import logging
import logging.config
import fileHandler as fH
from keycloackHandlerMemory import keycloackHandler
import registryHandler
import globalParamters
import pandas as pd
from twinCheck import TwinCheck
import datetime

# ✅ CRITICAL SOLVE GLOBALS ISSUE ==> initialize only once if inctance exists?
# ✅ Add functionality to force reload
# ✅ Refactor code into Classes and restructure programm
# ✅ Add functionality fo Multiple BPN's
# ✅ draw Statusbar
# ✅ Proxy settings variable
# ✅ Documentation
# Maybe: Write tests for checks(hard, dont know how yet)
# Maybe: get VANs
# TODO: Add more information to resultset to identify an object
# TODO: Refactor getTwinsByBPN force reload strategy (a pickl per bpn => abstraction a lot easier)


def writeTwinsAsCsv(twins, bpn):
    """this function writes the result in a human readable result to disk

    :param twins: list of twins
    :type twins: list
    :param bpn: bpn of the twins
    :type bpn: string
    """
    for i in twins:
        del i['shell']
    df = pd.DataFrame.from_dict(twins) 
    df.to_csv(f"{conf['check_output_filename']}_{bpn['company']}_{bpn['value']}_{datetime.datetime.now().strftime('%y%m%d')}.csv", index = False, header=True)


if __name__ == '__main__':
     
    # setup logging
    _logging_conf = fH.read_yaml(os.path.join(globalParamters.ROOT_DIR, 'logging.yaml'))
    logging.config.dictConfig(_logging_conf)
    _logging = logging.getLogger(__name__)

    # Writ start message
    _logging.info('#'*60)
    _logging.info('               START WEB SCRAPER')
    _logging.info('#'*60)

    #Load application configuration
    conf = fH.read_yaml(os.path.join(globalParamters.ROOT_DIR, 'settings.yaml'))
    globalParamters.set_conf(conf)
    _logging.info('-' * 60 )
    _logging.info(f'Configuration:')
    
    for key, value in globalParamters.CONF.items():
        _logging.info(f'   {key:23} {value}')
    _logging.info('-' * 60 )
    
    # Application Setup
    _logging.info('Application Setup:')
    TWINS_PICKL_PATH = os.path.join(globalParamters.ROOT_DIR, globalParamters.CONF['twins_pickl_filename'])
    
    if globalParamters.CONF['force_reload']:
        globalParamters.set_force_reload(True)
        fH.remove_file(TWINS_PICKL_PATH)
    _logging.info(f'   forced_reload\t\t{globalParamters.FORCE_RELOAD}')
    
    if 'proxies' in globalParamters.CONF:
        if globalParamters.CONF['proxies'] != {}:
            globalParamters.set_use_proxy(True)
        _logging.info(f'   use_proxy\t\t\t{globalParamters.USE_PROXY}')

    if len(globalParamters.CONF['bpn']) > 1: 
        globalParamters.set_multiple_bpns(True)
    _logging.info(f'   multiple_bpns\t\t{globalParamters.MULTIPLE_BPNS}')
    _logging.info('-' * 60 )


    # Application start
    kcH = keycloackHandler()
    rH = registryHandler.registryHandler(kcH)
    
    for bpn in conf['bpn']:
        shells = rH.getTwinsByBPN(bpn)
        tC = TwinCheck()
        shells = tC.check_twins(shells)
        writeTwinsAsCsv(shells, bpn)