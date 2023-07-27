"""
create conf file with list of .py files that sits in project folder, ID main file
CLI code that takes project folder path as input
reads conf file
makes Deploy folder, if not existing, copies files in list to Deploy
edits code, based on CICD notes to change paths, etc for VM
pulls the version number from main file
zips up code
sftp to VM

"""
import os
import re


def read_conf_file(config_path: str):
    """
    Reads and processes CICD configuration file, which consists of a list of
    file names. One will have a * identifying it as having the main code and
    from which the version number might be retrieved from header. Ignore
    commented lines (#).
    :param config_path: path to configuration file
    :return: list of file names and version number
    """
    conf_file = os.path.join(config_path, 'cicd_push.conf')
    file_list = []
    with open(conf_file) as cf:
        for line in cf:

            # ignore commented line
            if line[:1] == "#":
                continue

            file_str = line.rstrip('\n')

            # identify main file
            if file_str[-1] == "*":
                main_file = file_str[:-1]
                file_list.append(main_file)
            file_list.append(file_str)
            print(file_str)
    # retrieve version number
    main_f = os.path.join(config_path, main_file)
    with open(main_f) as mf:
        for line in mf:
            if "__version__" in line:
                ver_str = line.rstrip('\n')
                ver_str_list = ver_str.split('=')
                version_str = re.sub("[' ]", '', ver_str_list[1])

    return file_list, version_str
