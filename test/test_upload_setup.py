import pytest

from upload_setup import setup_folder_structure


def test_setup_folder_structure():
    setup_folder_structure('Setup_Test')

# if ((Test-Path -Path "C:\\Users\\TracyTD\\Setup_Test") -match $False) {md C:\\Users\\TracyTD\\Setup_Test}
