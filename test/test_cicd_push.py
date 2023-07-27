import pytest
import os
from cicd_push import cicd_push_main, read_conf_file, process_py_files_for_vm


def test_cicd_push_main():
    proj_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/Flight_File_Handler"
    deploy_path_str = cicd_push_main(proj_path)
    assert os.path.exists(deploy_path_str)

def test_read_conf_file():
    conf_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/Flight_File_Handler"
    list_files, version = read_conf_file(conf_path)
    assert list_files[0] == "data_gathering_utilities.py"
    assert version == '01.00.02'

def test_process_py_files_for_vm():
    conf_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/Flight_File_Handler"
    deploy_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/Flight_File_Handler/Deploy"
    list_files, version = read_conf_file(conf_path)
    r_line = process_py_files_for_vm(deploy_path, list_files)
    # assert r_line == "    db_file = 'fleet_manager.db'"
