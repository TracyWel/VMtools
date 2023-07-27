import pytest
from cicd_push import read_conf_file


def test_read_conf_file():
    conf_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/Flight_File_Handler"
    list_files, version = read_conf_file(conf_path)
    assert list_files[0] == "data_gathering_utilities.py"
    assert version == '01.00.02'
