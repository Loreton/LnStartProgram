#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# updated by ...: Loreto Notarantonio
# Version ......: 19-08-2019 12.35.42
import sys, os
from datetime import datetime
import json, yaml

# from . Ln_DotMap import DotMap as LnDict

##############################################################
# - DATA conversion
##############################################################

def str_to_dict(my_str):
    my_dict = json.loads(my_str)
    return my_dict

def json_to_dict(my_json):
    ''' notare .loads '''
    my_dict = json.loads(my_json)
    return my_dict


def dict_to_json(my_dict, indent=4, sort_keys=True):
    my_json = json.dumps(my_dict, indent=indent, sort_keys=sort_keys)
    return my_json



def dict_to_yaml(my_dict, sort_keys=True):
    # xx_json = json.dumps(my_dict, indent=4, sort_keys=True)
    my_json = json.dumps(my_dict, sort_keys=sort_keys)
    my_yaml = yaml.dump(yaml.load(my_json), default_flow_style=False)
    return my_yaml


##############################################################
# - READ - FILEs
##############################################################
def readJsonFile(filename):
   with open(filename, 'r') as fin:
       return(json.load(fin))


def readTextFile(filename, encoding='utf-8', exitOnError=True, logger=None):
    rows = []
    if not exitOnError:
        if not os.path.isfile(filename):
            return rows
    if logger:
        logger.info('reading file: {0}'.format(filename))
    with open(filename, 'r', encoding=encoding) as f:
        row = f.read()
    ''' if UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe0 in position 4163:
                invalid continuation byte
        try with encoding='latin-1'
    '''
    rows = [line.strip() for line in row.split('\n')]

    return rows


def readYamlFile(filename):
    with open(filename, 'r') as fin:
        return(yaml.load(fin))


def touch(local_file_path, atime=None, mtime=None):
    """ modify timestamp.
        se lo inserisco nella funzione download_file(...) non funziona.
        Nel senso che appena finisce lo script veien fatto il revert del valore.
    """
    _timestamp = hDrive.timeConvertion(drive_file['modifiedTime'])
    local_file_path = os.path.join(local.folder_path, drive_file['name'])
    # os.utime(local_file_path, (_timestamp['float'], _timestamp['float']))
    os.utime(local_file_path, (atime, mtime))

    # with open(local_file, 'ab') as f:
        # pass
        # os.utime(f.fileno(), (int(aTime), int(mTime)))
        # os.utime(f.fileno(), (aTime, mTime))
    print ("-> mtime after change  : "+ str(os.stat(local_file).st_mtime))
    print ("-> atime after change  : "+ str(os.stat(local_file).st_atime))        # os.utime(fname, (aTime, mTime))

##############################################################
# - WRITE - FILEs
##############################################################
def WriteTextFile(outFname, data=[]):
    nLines = 0
    newline = '\n'
    f = open(outFname, "w")
    for line in data:
        f.write('{0}{1}'.format(line, newline))
        nLines += 1
    f.close()
    return nLines



def writeYamlFile(file_out, my_data):
    if isinstance(my_data, dict):
        my_data = json.dumps(my_data, indent=4, sort_keys=True)
    my_yaml = yaml.dump(yaml.load(my_data), default_flow_style=False)
    writeFile(file_out, my_yaml)


def writeJsonFile(file_out, my_data):
    my_json = json.dumps(my_data, indent=4, sort_keys=True)
    writeFile(file_out, my_json)




def writeFile(file_out, data):
    with open(file_out, 'w') as f:
        f.write('{0}{1}'.format(data, '\n'))
    print ('\n\nfile: {} has been created.\n'.format(file_out))

def dictToFile(outFname, data={}):
    data = dict_to_json(data)
    f = open(outFname, "w")
    f.write('{0}{1}'.format(data, '\n'))
    f.close()




##############################################################
# - Parse Input
##############################################################
def ParseInput():
    import argparse
    # =============================================
    # = Parsing
    # =============================================
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(description='command line tool to test jboss ansible modules')
    parser.add_argument('--go', help='specify if command must be executed. (dry-run is default)', action='store_true')
    parser.add_argument('--log', help='Specify the debug level', required=False, default=-1, type=int, choices=[0,1,2,3])

    fileGroup = parser.add_mutually_exclusive_group(required=True)
    fileGroup.add_argument('--yaml-file', help='Specify yaml file to be processed')
    fileGroup.add_argument('--json-file', help='Specify json file to be processed')
    args = vars(parser.parse_args())

    if args['log'] < 0:
        args['log'] = False
        args['log_level'] = -1
    else:
        args['log_level'] = args['log']
        args['log'] = True

    # print args; sys.exit()
    return  args



def prompt(msg, validKeys='ENTER', exitKeys='x'):
    msg = "{0} [{1}] - ({2} to exit) ==> ".format(msg, validKeys, exitKeys)
    validKeys = validKeys.split('|')
    exitKeys = exitKeys.split('|')
    while True:
        choice      = input(msg).strip()
        choiceUPP   = choice.upper()
        if choice == '':    # diamo priorità alla exit
            if "ENTER" in exitKeys:
                sys.exit()
            elif "ENTER" in validKeys:
                return ''
            else:
                print('\n... please enter something\n')

        elif choice in exitKeys:
            print("Exiting on user request new.")
            sys.exit(1)

        elif choice in validKeys:
            break

        else:
            print('\n... try again\n')

    return choice



def readTreePath(root_path, folder):
    import pdb
    # pdb.set_trace()
    # Get list of folders three paths on computer
    root_dir = os.path.abspath(os.path.join(root_path, folder))
    root_len = len(root_path)+1
    if os.path.isdir(root_dir):
        local_tree_list = [folder]
    else:
        print("""
            root local directory [{}]
            doesn't exists.
            Please create it before continue.""".format(root_dir))
        sys.exit(1)

    for root, dirs, files in os.walk(root_dir, topdown=True):
        for name in dirs:
            local_tree_list.append(os.path.join(root[root_len:], name))

    return local_tree_list





def TreeList(root_path, folder):
    import pdb
    # pdb.set_trace()
    # Get list of folders three paths on computer
    root_dir = os.path.abspath(os.path.join(root_path, folder))
    root_len = len(root_path)+1
    if os.path.isdir(root_dir):
        local_tree_list = [folder]
    else:
        print("""
            root local directory [{}]
            doesn't exists.
            Please create it before continue.""".format(root_dir))
        sys.exit(1)

    for root, dirs, files in os.walk(root_dir, topdown=True):
        for name in dirs:
            local_tree_list.append(os.path.join(root[root_len:], name))

    return local_tree_list






def timeConvertion(value, sep='T', sourceGMT=False, returnGMT=False):
    '''
        return  LT/GMT value
    '''
    DT = {}
    LT = {}
    GMT = {}

    if isinstance(value, tuple):
        _dt = tuplexxx
    elif isinstance(value, float):
        _dt = datetime.fromtimestamp(value) # datetime.datetime(2018, 12, 5, 11, 16, 24, 800641)
    elif isinstance(value, datetime):
        _dt = value
    elif isinstance(value, str):
        _dt = datetime.strptime(value.rstrip('Z'), "%Y-%m-%dT%H:%M:%S.%f")
            # sommiamo l'offset all'ora GMT (nel caso sourceGMT==False)
        if value[-1] == 'Z' and not sourceGMT:
            offset = datetime.now() - datetime.utcnow()
            _dt += offset
    else:
        print (type(value))
        print (value)
        sys.exit()

    # ho considerato il tempo come LocalTime
    if sourceGMT: # portiamolo a LocalTime
        _gmt = _dt
        offset = datetime.now() - datetime.utcnow()
        _lt = _dt - offset
    else:
        _lt = _dt
        offset = datetime.now() - datetime.utcnow()
        _gmt = _dt - offset

    # DT['datetime']  = _dt   # mi da errore il logger    # datetime.datetime(2018, 12, 5, 11, 16, 24, 800641)

    if returnGMT:
        GMT['tuple']     = _gmt.timetuple() # time.struct_time(tm_year=2018, tm_mon=12, tm_mday=5, tm_hour=11, tm_min=16, tm_sec=24, tm_wday=2, tm_yday=339, tm_isdst=-1)
        GMT['float']     = float('{:.2f}'.format(_gmt.timestamp()))   # 1544004984.800641
        GMT['secs']      = int(_gmt.timestamp())                # 1544004984
        GMT['str']       = datetime.strftime(_gmt, "%Y-%m-%d %H:%M:%S")
        GMT['isoformat'] = _gmt.isoformat(sep=sep)
        GMT['time']      = _gmt.strftime("%H:%M:%S")
        GMT['time_f']    = _gmt.strftime("%H:%M:%S.%f")
        GMT['date']      = _gmt.strftime("%Y-%m-%d")
        DT = GMT

    else:
        LT['tuple']     = _lt.timetuple() # time.struct_time(tm_year=2018, tm_mon=12, tm_mday=5, tm_hour=11, tm_min=16, tm_sec=24, tm_wday=2, tm_yday=339, tm_isdst=-1)
        LT['float']     = float('{:.2f}'.format(_lt.timestamp()))   # 1544004984.800641
        LT['secs']      = int(_lt.timestamp())                # 1544004984
        LT['str']       = datetime.strftime(_lt, "%Y-%m-%d %H:%M:%S")
        LT['isoformat'] = _lt.isoformat(sep=sep)
        LT['time']      = _lt.strftime("%H:%M:%S")
        LT['time_f']    = _lt.strftime("%H:%M:%S.%f")
        LT['date']      = _lt.strftime("%Y-%m-%d")
        DT = LT

    # lnLogger.debug3('time conversion {0}'.format(value), DT)
    return DT

from math import log
def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    pow,n = min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)



def sizeof_fmt(num, suffix='B'):
    """Readable file size
    :param num: Bytes value
    :type num: int
    :param suffix: Unit suffix (optionnal) default = o
    :type suffix: str
    :rtype: str
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)



from math import log2
def filesizeFmt(size):
    _suffixes = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    # determine binary order in steps of size 10
    # (coerce to int, // still returns a float)
    order = int(log2(size) / 10) if size else 0
    # format file size
    # (.4g results in rounded numbers for exact matches and max 3 decimals,
    # should never resort to exponent values)
    return '{:.4g} {}'.format(size / (1 << (order * 10)), _suffixes[order])







# import yaml
# import os.path
'''
example.yaml
    a: 42
    b:
        - 12.53
        - 123.64

addfile.yaml
    - 32
    - [1, 2, 3]

    c: !include addfile.yaml
'''
'''
class Loader___(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)
        # print (data)
        # sys.exit()
        # return data


Loader.add_constructor('!include', Loader.include)

def resolve_yaml_vars___(data_dict):
    import re
    """
        variable_separator: {{ ... }}
        variable_format: {{ key0.key1.var_name}}
        keyx identify the dictionary_path to reach var_name

        we run findall but then process just one var at time
        replacing it with dictionary_data.
        ... then start findall again
    """


    data_str = json.dumps(data_dict)
    while True:
        var_names_list = re.findall(r'{{(.*?)}}', data_str)
        # remove empty separator
        var_names_list = [x for x in var_names_list if x.strip()]
        if not var_names_list:
            break

        # - get first var
        var = var_names_list[0]
        ptr = data_dict

        # - moving in dict depth
        for item in var.strip().split('.'):
            if item in ptr:
                ptr = ptr[item]
            else:
                msg = 'key: {} not found in the dictionary'.format(var)
                raise Exception('ERROR {}'.format(msg))


        str_to_replace = '{{' + var + '}}'
        data_str = data_str.replace(str_to_replace, str(ptr))

    resolved_dict = json.loads(data_str)
    return resolved_dict
'''