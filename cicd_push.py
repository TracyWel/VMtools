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
import shutil


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
            else:
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


def process_prod_line(line, p_str):
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
def process_py_files_for_vm(deployment_path, py_files):
    """
    test case
    # db_file = 'fleet_manager.db'  # CICD:production_1
    db_file = 'fleet_manager_e2etest_large.db' # CICD:testing_1

    :return:
    """
    print('\nprocess_py_files_for_vm\n')
    line_1 = "    # db_file = 'fleet_manager.db'  # CICD:production_1"
    line_2 = "db_file = 'fleet_manager_e2etest_large.db' # CICD:testing_1"
    prod_str = 'CICD:production'
    testing_str = 'CICD:testing'
    for py_file in py_files:
            p_file = os.path.join(deployment_path, py_file)

            if prod_str in open(p_file).read():
                print(py_file)
                py_file_out = f'new_{py_file}'
                p_file_out = os.path.join(deployment_path, py_file_out)

                with open(p_file_out, 'w') as pfo:

                    with open(p_file, 'r') as pf:
                        for line in pf:
                            write_line = True
                            ready_line = line

                            # generate production line
                            if prod_str in line:
                                ready_line = process_prod_line(line, prod_str)
                                print(ready_line)
                                write_line = True

                            # skip testing lines
                            if testing_str in line:
                                write_line = False

                            if write_line:
                                pfo.write(ready_line)


def cicd_push_main(project_path):
    """
    Prepares code and pushes it to the VM for deployment.

    1. copy relevant code to deploy folder, based on list in config file
    2. process code (change paths mostly)
    3. create zip file
    4. sftp to VM

    :return:
    """
    # project_path will be defined by arg parse

    # process files
    # zip
    # sftp files

    # check existence of deploy folder
    deploy_folder = 'Deploy'
    deploy_path = os.path.join(project_path, deploy_folder)
    if not os.path.exists(deploy_path):
        os.makedirs(deploy_path)

    # read config file
    list_files, version = read_conf_file(project_path)

    # copy files to deploy folder
    for f in list_files:
        file_to_copy = os.path.join(project_path, f)
        shutil.copy(file_to_copy, deploy_path)

    # process file changes
    process_py_files_for_vm(deploy_path, list_files)

    return deploy_path