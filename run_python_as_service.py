import os
import shutil
import logging
from typing import List
import time
import datetime as dt


def filter_by_extension(onlyfiles: List[str], extension_str: str):
    """
    Remove files from the list that lack the specified extension. Handles
    lower or upper case (eg .csv and .CSV).

    :param onlyfiles: the list of files in the folder
    :param extension_str: file extension match string, current a/c (fleet table)
    :return: onlyfiles list trimmed to include only the specified extension
    """

    if not extension_str:
        return onlyfiles

    list_index = 0
    while len(onlyfiles) > 0 and list_index < len(onlyfiles):
        file_split_list = onlyfiles[list_index].split('.')
        if file_split_list[-1].upper() != extension_str.upper():
            onlyfiles.pop(list_index)
        else:
            list_index += 1

    return onlyfiles


def move_airsync_files():
    current_time = dt.datetime.now()
    file_path = 'U:'
    destination_path = 'F:/sftp/AirSync.staging'
    log_file = os.path.join(destination_path, 'staging.log')
    logging.basicConfig(filename=log_file, filemode='a',
                        encoding='utf-8', level=logging.DEBUG)

    onlyfiles_csv = filter_by_extension(os.listdir(file_path), 'csv')
    logging.info('move_airsync_files: $s files to move',len(onlyfiles_csv))

    for f in onlyfiles_csv:
        shutil.move(os.path.join(file_path, f), os.path.join(destination_path, f))
        logging.info('move_airsync_files: at time %s, moved %s, to %s',
                     current_time, f, destination_path)


def start_process():
    keep_running = True
    while keep_running:
        move_airsync_files()
        time.sleep(10)


if __name__ == "__main__":
    start_process()
