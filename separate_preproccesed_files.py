import os
import sys
import shutil
from argparse import ArgumentParser
import logging


def parse_command_arguments(argv):
    """
    Parse command line arguments

    param: argv: command line arguments
    """
    parser = ArgumentParser(
        description="separates CSV flight files based on whether TD_ headers"
                    "are found in the header line")
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        default=' ',
        help="Path to input CSV files",
        type=str
    )
    parser.add_argument(
        "-o",
        "--output_path",
        required=True,
        default=' ',
        help="Path to move files that have already been processed",
        type=str
    )
    args = parser.parse_args()
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    logging.info('parse_command_arguments: Input files path: %s', args.input_path)
    logging.info('parse_command_arguments: Output path: %s', args.output_path)

    return args


def separate_preprocessed_files_main(argv):
# def separate_preprocessed_files_main():

    command_line_arguments = parse_command_arguments(argv)
    input_path = command_line_arguments.input_path
    output_path = command_line_arguments.output_path

    # input_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/VMtools/data"
    # output_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/VMtools/result"

    target_list = []

    # Iterate over all entries in the input directory
    for entry in os.listdir(input_path):
        file_path = os.path.join(input_path, entry)
        # Check if it's a file and ends with .txt
        if os.path.isfile(file_path) and file_path.endswith('.csv'):
            with open(file_path, 'r') as file:
                line_ind = 0
                for line in file:
                    if "TD_" in line:
                        target_list.append(file_path)
                        break
                    line_ind += 1
                    if line_ind > 10:
                        break

    # Move files from the list to the output directory
    for file_path in target_list:
        shutil.move(file_path, os.path.join(output_path, os.path.basename(file_path)))
        print(f"File moved: {file_path}")


if __name__ == "__main__":
    separate_preprocessed_files_main(sys.argv[1:])
    # separate_preprocessed_files_main()
