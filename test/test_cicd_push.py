import pytest
import os
from cicd_push import cicd_push_main, read_conf_file, process_py_files_for_vm, \
process_prod_line, zip_deploy


def test_cicd_push_main():
    proj_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/Flight_File_Handler"
    deploy_path_str = cicd_push_main(proj_path)
    assert os.path.exists(deploy_path_str)


def test_read_conf_file():
    conf_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/Flight_File_Handler"
    list_files, version = read_conf_file(conf_path)
    assert list_files[0] == "data_gathering_utilities.py"
    assert version == '01.00.02'


def test_process_prod_line():
    """
    test case
    # db_file = 'fleet_manager.db'  # CICD:production_1
    db_file = 'fleet_manager_e2etest_large.db' # CICD:testing_1
    :return:
    """
    new_line = "    # db_file = 'fleet_manager.db'  # CICD:production_1 "
    prod_str = 'CICD:production'
    ready_line = process_prod_line(new_line, prod_str)
    assert ready_line == "    db_file = 'fleet_manager.db'\n"


def test_process_py_files_for_vm():
    dep_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/Flight_File_Handler/Deploy"
    file_list = ['flight_file_handler.py']
    process_py_files_for_vm(dep_path, file_list)


def test_zip_deploy():
    des_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/Flight_File_Handler"
    dep_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/Flight_File_Handler/Deploy"
    zip_deploy(des_path, dep_path)
