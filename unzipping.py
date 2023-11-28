__author__ = 'John Martinez'
__copyright__ = 'Copyright 2022, 2023 Truth Data Insights'
__credits__ = 'John Martinez'
__version__ = '00.00.10'
__maintainer__ = 'John Martinez, Tracy Welterlen'
__email__ = 'john@truthdata.net, tracy@truthdata.net'
__status__ = 'Trial'

"""
This utility unzips files sent in a zip folder to a designated folder.
The original zip file can be moved to another (backup) folder after the 
fact. A clean up function deletes backed up zip files older than one
month. 
"""

import zipfile
import shutil
import argparse
import datetime as dt
from dateutil.relativedelta import *
import os
from typing import List
import sys


def parse_command_arguments(argv):
    parser = argparse.ArgumentParser(
        description="")
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        default=' ',
        help="Path to zip files",
        type=str
    )
    parser.add_argument(
        "-t",
        "--target_path",
        required=True,
        default=' ',
        help="unzipped folder",
        type=str
    )
    parser.add_argument(
        "-b",
        "--backup_path",
        required=True,
        default=' ',
        help="back up folder",
        type=str
    )
    return parser.parse_args()


def unzipping(dir_path: str, target_path: str):
    """
    Unzips files and put them in to the target path
    :param dir_path: the path were the zip files are
    :param target_path: where unzipped files are to be placed
    :return: List of zip folders that have been unzipped
    """

    processed_files = []  # Initialize a list to keep track of processed files
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    for file in os.listdir(dir_path):
        if file.endswith('.zip') and file not in processed_files:
            with zipfile.ZipFile(os.path.join(dir_path, file), 'r') as zip_file:
                zip_file.extractall(target_path)  # Extract the contents of the new ZIP file

            processed_files.append(file)  # Add the processed file to the list
    return processed_files


def move_zip(dir_path: str, backup_path: str, zip_lists: List[str]):
    """
    Moves zip files to a backup folder
    :param dir_path: the path were the zip files are
    :param backup_path: where the zip files will be backed up to
    :param zip_lists: list of zip files to put into back up
    :return: none
    """
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
    for file in zip_lists:
        shutil.move(os.path.join(dir_path, file), os.path.join(backup_path, file))


def retrieve_files(path: str):
    return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def cleanup_old_logs(log_path: str):
    """
    As the name suggests, this function deletes old log files
    :param log_path: path to the log files
    :return: none
    """
    # delete log files over one month old
    month_ago = dt.datetime.now() + relativedelta(months=-1)
    n_files = 0

    for f in retrieve_files(log_path):
        log_file_created = dt.datetime.fromtimestamp(os.path.getctime(f))
        if log_file_created < month_ago:  # Older than one month ago
            os.remove(f)
            n_files += 1


# def unzip_main():
def unzip_main(argv):
    command_line_arguments = parse_command_arguments(argv)
    zip_file_path = command_line_arguments.input_path
    unzipped_file_path = command_line_arguments.target_path
    backup_path = command_line_arguments.backup_path
    # zip_file_path = 'C:/Users/John Martinez/OneDrive - Truth Data Insights/Software/Unzip/Raw Data'  # Use actual path to your ZIP file
    # unzipped_file_path = 'C:/Users/John Martinez/OneDrive - Truth Data Insights/Software/Unzip/Raw Data/.upload'
    # backup_path = 'C:/Users/John Martinez/OneDrive - Truth Data Insights/Software/Unzip/Raw Data/.backup'
    unzipped_files = unzipping(zip_file_path, unzipped_file_path)
    move_zip(zip_file_path, backup_path, unzipped_files)
    cleanup_old_logs(backup_path)  # Clean up all the zip files after a month


if __name__ == "__main__":
    unzip_main(sys.argv[1:])
    # unzip_main()
