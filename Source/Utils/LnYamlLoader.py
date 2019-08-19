#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# updated by ...: Loreto Notarantonio
# Version ......: 24-06-2019 09.07.33
import sys
import os
import re
import json
import yaml
from pathlib import Path


logger = None
def log_it(*data):
    if logger:
        logger(*data)
    else:
        print (*data)

"""
    variable_identifier: <PREFIX> ... <SUFFIX>
    variable_name_format:
        {{     fname:key0.key1.keyn}}       - get data from fname.yml fname.yaml
        {{ fname.xyz:key0.key1.keyn}}   - get data from fname.xyz
        {{       env:key0.key1.key...n}}       - get data from environment variables
        {{      key0.key1.key...n}}       - get data from internal data

    keyx identify the dictionary_path to be searched

    we run findall but we process just one var at time
    replacing it with dictionary_data.
    ... then start findall again
"""




def LoadYamlFile(filename):
    global base_dir
    processed_vars = [] # variables already processed
    base_dir = os.path.split(filename)[0] # directory of current file

    if not Path(filename).exists():
        print (filename, 'NOT FOUND')
        sys.exit(1)

    with open(filename, 'r') as f:
        data_str = f.read() # single string

    """ removal of all commented lines to avoid solving
    variables that could create errors"""
    rows = []
    for line in data_str.split('\n'):
        if not line.strip(): continue
        if line.strip()[0]=='#': continue
        rows.append(line)

    result = '\n'.join(rows)
    content = yaml.safe_load(result)
    return content


def processYamlData(data, prefix=r'${', suffix=r'}', errorOnNotFound=True, mylogger=None):
    assert isinstance(data, (dict, str))
    global data_str, already_read_files, logger, error_OnNotFound
    logger = mylogger
    error_OnNotFound = errorOnNotFound
    already_read_files = {}

    data_str = data if isinstance(data, str) else json.dumps(data)
    processed_vars = [] # variables already processed

    _prefix = prefix.replace('$', '\\$')
    _suffix = suffix.replace('$', '\\$')
    """prefix - suffix: variable must be suffixed by non unicode
                        characters to avoid parsing errors
                        tested and cut: $, {}, §, ...
    """
    # - search for variables
    strToFind = _prefix + r'(.*?)' + _suffix
    while True:
        var_names_list = re.findall(strToFind, data_str)
        var_names_list = [x for x in var_names_list if x.strip()] # ignore empty vars --> {{ }}
        var_names_list = [x for x in var_names_list if x not in processed_vars] # ignore already processed vars
        if not var_names_list: # process completed
            break

        var_name = var_names_list[0] # get the first variable
        var_value = _decode_variable(var_name) # decode and search for it
        if var_value:   # variable value FOUND
            # remove DQuote around the string created by json.dumps
            DQ = '"'
            _new_data = json.dumps(var_value, indent=4, sort_keys=True).strip('"')
            str_to_replace = prefix + var_name + suffix
            data_str = data_str.replace(str_to_replace, _new_data)
        else:
            if error_OnNotFound:
                msg = 'Variable {0} NOT FOUND'.format(prefix + var + suffix)
                logger.error(msg)
                sys.exit()
            else:
                processed_vars.append(var_name)


    return yaml.load(data_str)
    # return yaml.safe_load(data_str)


def _decode_variable(var_name):
    _dict = yaml.load(data_str) # read currente data as dict

    if ':' in var_name:
        _fname, d_path = var_name.strip().split(':', 1) # format filename:key1.key2....
        if _fname.lower() in ('env:'): # format env:varname
            _value = os.environ.get(d_path, None)
            logger.debug(d_path, _value)
            # if not _value and error_OnNotFound:
            if _value and _value[1] == ':':
                _value = Path(_value).resolve() # elimina tutti i \\\\ eccedenti
            elif not _value and error_OnNotFound:
                print('variable: "{}" NOT found.'.format(d_path))
                sys.exit(1)

            return str(_value)

        else:
            if _fname in already_read_files:
                _dict = already_read_files[_fname]

            # - altrimenti leggilo
            else:
                filename, ext = os.path.splitext(_fname)
                extensions = [ext] if ext else ['.yaml', '.yml']
                # read file
                _dict = None
                for ext in extensions:
                    file = os.path.abspath(os.path.join(base_dir, '{0}{1}'.format(filename, ext)))
                    if os.path.isfile(file):
                        with open(file, 'r') as fin:
                            _dict = yaml.load(fin)
                        already_read_files[_fname] = _dict
                        break

                if _dict is None:
                    raise IOError('File: {} NOT FOUND!'.format(file))


    elif '.' in var_name:
        d_path = var_name

    else:
        # un variabile senza prefisso... skip it
        return None


    # - moving through the dict tree
    ptr = _dict
    for item in d_path.strip().split('.'):
        if item in ptr:
            ptr = ptr[item]
        else:
            msg = 'key: {} not found in the dictionary'.format(d_path)
            raise Exception('ERROR {}'.format(msg))

    if ptr[1] == ':':
        ptr = Path(ptr).resolve() # elimina tutti i \\\\ eccedenti
        # if not ptr.exists() and errorOnPathNotFound:
        #     print('path: "{}" NOT found.'.format(ptr))
        #     sys.exit(1)

    return str(ptr)






def LoadYamFile_Prev(filename, prefix=r'${', suffix=r'}', errorOnNotFound=True, logger=None):
    _prefix = prefix.replace('$', '\\$')
    _suffix = suffix.replace('$', '\\$')
    """prefix - suffix: variable must be suffixed by non unicode
                        characters to avoid parsing errors
                        tested and cut: $, {}, §, ...
    """
    global data_str, base_dir, already_read_files
    already_read_files = {}
    processed_vars = [] # variables already processed
    base_dir = os.path.split(filename)[0] # directory of current file

    with open(filename, 'r') as f:
        data_str = f.read() # single string

    """ removal of all commented lines to avoid solving
    variables that could create errors"""
    rows = []
    for line in data_str.split('\n'):
        if not line.strip(): continue
        if line.strip()[0]=='#': continue
        rows.append(line)

    data_str = '\n'.join(rows)

    # - search for variables
    strToFind = _prefix + r'(.*?)' + _suffix
    while True:
        var_names_list = re.findall(strToFind, data_str)
        var_names_list = [x for x in var_names_list if x.strip()] # ignore empty vars --> {{ }}
        var_names_list = [x for x in var_names_list if x not in processed_vars] # ignore already processed vars
        if not var_names_list: # process completed
            break

        var_name = var_names_list[0] # get the first variable
        # if var_name in ['VARS.Ln_RootDir']:
        #     var_name = var_name
        var_value = _decode_variable(var_name) # decode and search for it
        if var_value:   # variable value FOUND
            # remove DQuote around the string created by json.dumps
            DQ = '"'
            _new_data = json.dumps(var_value, indent=4, sort_keys=True).strip('"')
            str_to_replace = prefix + var_name + suffix
            data_str = data_str.replace(str_to_replace, _new_data)
        else:
            if errorOnNotFound:
                msg = 'Variable {0} NOT FOUND'.format(prefix + var + suffix)
                if logger:
                    logger.error(msg)
                else:
                    print(msg)
                sys.exit()
            else:
                processed_vars.append(var_name)


    return yaml.load(data_str)
    # return yaml.safe_load(data_str)




def load_yaml2(filename):
    path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')
    def path_constructor(loader, node):
        return os.path.expandvars(node.value)

    class EnvVarLoader(yaml.SafeLoader):
        pass

    EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
    EnvVarLoader.add_constructor('!path', path_constructor)

    c = None
    with open(filename) as f:
        c = yaml.load(f, Loader=EnvVarLoader)

    return c





def _include_variable(loader, node):
    # seq = loader.construct_sequence(node)
    data_str = loader.construct_scalar(node)
    prefix=r'_{{'
    suffix=r'}}_'

    # - search for variables
    strToFind = prefix + r'(.*?)' + suffix
    while True:
        var_names_list = re.findall(strToFind, data_str)
        var_names_list = [x for x in var_names_list if x.strip()] # ignore empty vars --> {{ }}
        if not var_names_list: # process completed
            break

        var = var_names_list[0] # - get the first variable
        ptr = _decode_variable(var) # - decode and search for it

        # .strip('"')... remove DQuote around the string created by json.dumps
        _new_data = json.dumps(ptr, indent=4, sort_keys=True).strip('"')
        str_to_replace = prefix + var + suffix
        data_str = data_str.replace(str_to_replace, _new_data)

    return yaml.load(data_str)























## define custom tag handler
def join(loader, node):
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])

def joinPath(loader, node):
    seq = loader.construct_sequence(node)
    return '/'.join([str(i) for i in seq])

def upper(loader, node):
    data = loader.construct_scalar(node)
    return data.upper()

def evaluate(loader, node):
    data = loader.construct_scalar(node)
    return eval(data)

## register the tag handler
yaml.add_constructor('!join', join)
yaml.add_constructor('!joinPath', joinPath)
yaml.add_constructor('!upper', upper)
yaml.add_constructor('!eval', evaluate)
# yaml.add_constructor('!incl', _include_variable)




if __name__ == '__main__':
    my_data = '''
        # servono da riferimento ma per ogni riga verrà creata una variabile di ambiente
        VARS:
            Ln_Drive      : ${Ln_AAA}  # creata at run time
            Ln_RootDir    : ${Ln_AAA}  # creata at run time
            Ln_RootDir1   : Ciao  # creata at run time
            Ln_ProgramDIR : ${Ln_AAA}  # creata at run time - directory dello script


            Ln_StartDir        : ${VARS.Ln_RootDir}/LnStart
            Ln_LoretoDir       : ${VARS.Ln_RootDir}/Loreto
            Ln_FreeDir         : ${VARS.Ln_RootDir}/LnFree
            Ln_LeslaDir        : ${VARS.Ln_RootDir}/Lesla


            Ln_StartDir1       : _${VARS.Ln_RootDir1}_/LnStart
            Ln_LoretoDir1      : _${VARS.Ln_RootDir}_/Loreto
            Ln_FreeDir1        : _${VARS.Ln_RootDir1}_/LnFree
            Ln_LeslaDir1       : _${VARS.Ln_StartDir1}_/Lesla

            Ln_StartDir2       : ${VAR.myVAR}/LnStart
            Ln_LoretoDir2      : ${VAR.myVAR}/Loreto
            Ln_FreeDir2        : ${VAR.myVAR}/LnFree
            Ln_LeslaDir2       : ${VAR.myVAR}/Lesla
    '''

