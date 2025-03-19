from os import listdir
from os.path import isfile, join, exists
import sys
from argparse import ArgumentParser
import logging
import pandas as pd


# recover G1000 system software version
def parse_command_arguments(argv):
    """
    Parses CLI inputs
    :param argv: command line arguments
    :return:
    """
    parser = ArgumentParser(
        description="Recovers Garmin1000 software version numbers from files.")
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        default=' ',
        help="Path to the files",
        type=str
    )
    parser.add_argument(
        "-o",
        "--output_path",
        required=True,
        default=' ',
        help="Path to write output",
        type=str
    )
    args = parser.parse_args()
    logging.info('parse_command_arguments: file path: %s', args.input_path)

    if not args.input_path:
        logging.info('parse_command_arguments: ERROR: required path not set %s',
                     args.input_path)
        sys.exit(-1)

    return args


# file_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/AGL/AGL/data_LFN/.backup"
def get_version_num(argv):

    logging.info('cicd_push_main: Begin processing')

    command_line_arguments = parse_command_arguments(argv)
    file_path = command_line_arguments.input_path
    out_path = command_line_arguments.output_path

    onlyfiles = [f for f in listdir(file_path) if isfile(join(file_path, f))]

    software_str = 'system_id='  # system
    # software_str = 'system_software_part_number='  # software

    version_list = []
    for g_file in onlyfiles:
        with open(join(file_path, g_file)) as g1000_f:
            first_line = g1000_f.readline()
            index = -1
            if software_str in first_line:
                index = first_line.find(software_str)
            else:
                continue
            # soft_id = first_line[index + 30: index + 41]  # software

            # system
            temp_id = first_line[index + 11: index + 32]
            split_list = temp_id.split(',')
            soft_id = split_list[0].replace('"', "")
        print(g_file, soft_id)
        version_list.append(soft_id)

    unique_ids_list = list(set(version_list))
    print(f'Unique IDs: {unique_ids_list}')

    output_df = pd.DataFrame(
        {'Filenames': onlyfiles,
         'Versions': version_list
         })
    output_df.to_csv(join(out_path, 'g1000_version.csv'))


if __name__ == "__main__":
    get_version_num(sys.argv[1:])
