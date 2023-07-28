__author__ = 'Tracy Welterlen'
__copyright__ = 'Copyright 2023, Truth Data Insights'
__credits__ = 'Tracy Welterlen'
__version__ = '00.00.01'
__maintainer__ = 'Tracy Welterlen'
__email__ = 'tracy@truthdata.net'
__status__ = 'Development'
"""
This is part of a homemade Continous Integration / Continuous Deployment (CICD)
system. It prepares the necessary files for a code to be deployed to the 
production system.

It uses a configuration file, called cicd.conf, with a list of .py files 
that sits in project folder. The main code file is identified with .py*
Any lines in cicd.conf starting with # are ignored.

The CLI takes the project folder path as input then:
1) reads the configuration file
2) makes Deploy folder, if not existing, and copies files in list to Deploy
3) edits code, based on CICD notes to change paths (see doc string for 
process_prod_line), etc for VM
4) pulls the version number from main file
5) zips up code
6) sftps the zip file to VM

"""
import os
import sys
import re
import shutil
from typing import List
import logging
from argparse import ArgumentParser
import os
import zipfile

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


def parse_command_arguments(argv):
    """
    Parses CLI inputs
    :param argv: command line arguments
    :return:
    """
    parser = ArgumentParser(
        description="Prepares the necessary files for a code to be deployed "
                    "to the production system.")
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        default=' ',
        help="Path to the project files",
        type=str
    )
    args = parser.parse_args()
    logging.info('parse_command_arguments: Project path: %s', args.input_path)

    if not args.input_path:
        logging.info('parse_command_arguments: ERROR: required path not set %s',
                     args.input_path)
        sys.exit(-1)

    if not os.path.exists(os.path.join(args.input_path, 'cicd_push.conf')):
        logging.info('parse_command_arguments: ERROR: configuration file '
                     'missing %s/cicd_push.conf', args.input_path)
        sys.exit(-1)

    return args


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
            logging.info('read_conf_file: %s', file_str)

            # identify main file
            if file_str[-1] == "*":
                main_file = file_str[:-1]
                file_list.append(main_file)
            else:
                file_list.append(file_str)

    # retrieve version number
    main_f = os.path.join(config_path, main_file)
    with open(main_f) as mf:
        for line in mf:
            if "__version__" in line:
                ver_str = line.rstrip('\n')
                ver_str_list = ver_str.split('=')
                version_str = re.sub("[' ]", '', ver_str_list[1])

    return file_list, version_str


def process_prod_line(line: str, p_str: str):
    """
    Modifies lines in python files that include specific comments.

      # CICD:production_1
    Lines with this at the end (two spaces before the #) will be prepared for
    production use. The comment is removed, the line is uncommented out if that
    is the case and a newline character is added. Leading indentation is preserved.

    The number at the end of the comment indicates how many lines are
    impacted, eg. multiple continuation lines. At the moment (20230728) this
    feature is not coded.


    :param line: the current line of code, identified as having the production
    comment in it
    :param p_str: the production comment:  # CICD:production_1
    :return: the modified line of code
    """

    clean_line = line.rstrip()
    line_list = []
    # find number of relevant lines
    index = clean_line.find(p_str)
    prod_split_list = clean_line[index:].split('_')
    num_lines = int(prod_split_list[1])
    # line_list.append(clean_line)
    if num_lines > 1:
        for i in range(num_lines - 1):
            # TODO: flesh this out later
            # read line
            # append to list
            pass

    if num_lines > 1:
        # TODO: flesh this out later
        pass
    else:
        # remove CICD flag
        temp_line = re.sub(r'  # CICD:production_\d+', '', clean_line)
        bare_line = f'{temp_line}\n'

        if '#' in bare_line:
            uncommented_line = re.sub(r'# ', '', bare_line)
        else:
            uncommented_line = bare_line

    return uncommented_line


# def process_py_files_for_vm():
def process_py_files_for_vm(deployment_path: str, py_files: List[str]):
    """
    Modifies python files to prepare for production.
    Lines with  # CICD:production_1 are prepared for use.
    Lines with  # CICD:testing_1 are deleted.

    :param deployment_path: path to deployment folder
    :param py_files: list of python files from cicd.conf
    :return: none
    """
    prod_str = 'CICD:production'
    testing_str = 'CICD:testing'
    new_files = []
    for py_file in py_files:
            p_file = os.path.join(deployment_path, py_file)

            if prod_str in open(p_file).read():
                logging.info('process_py_files_for_vm: %s', py_file)
                py_file_out = f'new_{py_file}'
                p_file_out = os.path.join(deployment_path, py_file_out)
                pair_list = [py_file, py_file_out]
                new_files.append(pair_list)

                with open(p_file_out, 'w') as pfo:

                    with open(p_file, 'r') as pf:
                        for line in pf:
                            write_line = True
                            ready_line = line

                            # generate production line
                            if prod_str in line:
                                ready_line = process_prod_line(line, prod_str)
                                logging.info('process_py_files_for_vm: %s', ready_line)
                                write_line = True

                            # skip testing lines
                            if testing_str in line:
                                write_line = False

                            if write_line:
                                pfo.write(ready_line)

    # replace old with new files
    for pair in new_files:
        os.remove(os.path.join(deployment_path, pair[0]))
        os.rename(os.path.join(deployment_path, pair[1]),
                  os.path.join(deployment_path, pair[0]))


def zip_deploy(dest_path: str, source_dir: str):
    """
    Zip files for deploy

    :param dest_path: location to write the zip file
    :param source_dir: location of the files to be zipped
    :return: none
    """

    zf = zipfile.ZipFile(os.path.join(dest_path, 'vm_deploy.zip'), "w")
    for dirname, subdirs, files in os.walk(source_dir):
        for filename in files:
            file_zip = os.path.join(dirname, filename)
            zf.write(file_zip, os.path.basename(file_zip))
    zf.close()


def cicd_push_main(argv):
    """
    Prepares code and pushes it to the VM for deployment.

    1. copies relevant code to deploy folder, based on list in config file
    2. process code (change paths mostly)
    3. create zip file
    4. sftp to VM

    :return:
    """
    logging.info('cicd_push_main: Begin processing')

    command_line_arguments = parse_command_arguments(argv)
    project_path = command_line_arguments.input_path

    # check existence of deploy folder
    deploy_folder = 'Deploy'
    deploy_path = os.path.join(project_path, deploy_folder)
    if not os.path.exists(deploy_path):
        os.makedirs(deploy_path)

    # read config file
    list_files, version = read_conf_file(project_path)
    logging.info('cicd_push_main: file list\n%s', list_files)

    # copy files to deploy folder
    for f in list_files:
        file_to_copy = os.path.join(project_path, f)
        shutil.copy(file_to_copy, deploy_path)
    logging.info('cicd_push_main: files moved to deploy folder')

    # process file changes
    process_py_files_for_vm(deploy_path, list_files)
    logging.info('cicd_push_main: files processed')

    # zip
    zip_deploy(project_path, deploy_path)
    logging.info('cicd_push_main: files zipped')

    # sftp zip


if __name__ == "__main__":
    cicd_push_main(sys.argv[1:])
