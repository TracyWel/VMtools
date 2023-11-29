import os
import sys
import logging
import shutil
from argparse import ArgumentParser


def parse_command_arguments(argv):
    parser = ArgumentParser(
        description="Processes agl_main for building and running, which"
                    "involves some commenting and uncommenting a few lines")
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        default=' ',
        help="Path to agl_main.py",
        type=str
    )
    parser.add_argument(
        "-m",
        "--mode",
        required=True,
        default='b',
        help="Mode to be executed: b = build, r = run",
        type=str
    )
    args = parser.parse_args()
    logging.info('parse_command_arguments: Input files path: %s', args.input_path)
    logging.info('parse_command_arguments: Execution mode: %s', args.mode)
    return args


def modify_line(f, mode, m_flag, mod_text, indent):

    if mode == m_flag:
        # overwrite line with uncommented version
        logging.info('modify_line: %s uncommented', mod_text)
        return f'{indent}{mod_text}\n'
    else:
        # overwrite with commented version
        logging.info('modify_line: %s commented out', mod_text)
        return f'{indent}# {mod_text}\n'


def move_files(old_f_name, new_f_name, dest_path):
    """
    Moves a list of files

    :param old_f_name: list of the new file names
    :param new_f_name: list of the new file names
    :param dest_path: path to move files to
    """
    new_pathnfile = (os.path.join(dest_path, new_f_name))
    old_pathnfile = (os.path.join(dest_path, old_f_name))
    shutil.move(old_pathnfile, new_pathnfile)
    logging.info('move_files: %s to %s', old_f_name, new_f_name)


def prep_for_docker_build_main(argv):
# def prep_for_docker_build_main():

    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    command_line_arguments = parse_command_arguments(argv)
    input_path = command_line_arguments.input_path
    ex_mode = command_line_arguments.mode

    # input_path = 'C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/AGL/AGL'
    # ex_mode = 'b'

    logging.info('prep_for_docker_build_main: running in %s mode', ex_mode)

    py_file = 'agl_main.py'
    # py_file = 'samp_code.py'
    py_out_file = 'new_code.py'
    line_str = ['import rasterio',
                'clipfile = get_geotiff(rect)',
                'elev_list_rect, agl_list_rect = compute_agl(clipfile, pts_df)',
                'elev_list_rect, agl_list_rect = compute_fake_agl(pts_df)'
                ]
    mod_flag = ['b', 'b', 'b', 'r']
    indent = ['', '    ', '    ', '    ']

    logging.info('main: editing %s in %s', py_file, input_path)

    # read whole file in as list of lines
    with open(os.path.join(input_path, py_file), "r") as f:
        lines = f.readlines()

    logging.info('main: file read')

    with open(os.path.join(input_path, py_out_file), "w") as f:
        # step through lines and make appropriate changes
        for line in lines:
            # check for lines of interest
            for index, text in enumerate(line_str):
                if text in line:
                    new_line = modify_line(f, ex_mode, mod_flag[index],
                                           text, indent[index])
                    break
                else:
                    new_line = line
            f.write(new_line)

    logging.info('main: file %s written', py_out_file)

    # rename files
    backup_file = f'old_{py_file}'
    move_files(py_file, backup_file, input_path)
    move_files(py_out_file, py_file, input_path)


if __name__ == "__main__":
    prep_for_docker_build_main(sys.argv[1:])
