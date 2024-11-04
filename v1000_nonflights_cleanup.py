import sys
import os
import logging
from argparse import ArgumentParser
from typing import List


def parse_command_arguments(argv):
    parser = ArgumentParser(
        description="Clean up Appareo files that are not flights")
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        default=' ',
        help="Path to input flight data files",
        type=str
    )
    return parser.parse_args()


def delete_v1000_nonflights(f_path: str, f_list: List[str]):
    """
    Deletes V1000 files that are nonflights. This is evident by the lack
    of an airport designation replaced by multiple underscores and a
    file size less than 20 kb.

    :param f_path: path to files
    :param f_list: list of files
    :return:
    """
    del_list = []
    for f in f_list:
        f_size = os.path.getsize(os.path.join(f_path, f))
        if '___' in f or f_size < 20000:
            del_list.append(f)
            os.remove(os.path.join(f_path, f))
    return del_list


def v1000_nonflight_cleanup(argv):
    """
    Main function for deleting Vision1000 nonflights
    :param argv: parsed arguments
    :return: none
    """
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    logging.info('\n v1000_nonflight_cleanup: Starting process')

    command_line_arguments = parse_command_arguments(argv)
    input_path = command_line_arguments.input_path

    file_list = [f for f in os.listdir(input_path)
                 if os.path.isfile(os.path.join(input_path, f))]

    # filter for V1000 files
    v1000_filtered_file_list = [f for f in file_list if "converted" in f]

    deleted_files = delete_v1000_nonflights(input_path, v1000_filtered_file_list)

    logging.info('\n v1000_nonflight_cleanup: files deleted:\n %s', deleted_files)
   

if __name__ == "__main__":
    v1000_nonflight_cleanup(sys.argv[1:])