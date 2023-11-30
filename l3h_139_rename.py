import sys
import os.path
import pandas as pd
from argparse import ArgumentParser
import logging


def parse_command_arguments(argv):
    """
    Parse command line arguments

    param: argv: command line arguments
    """
    parser = ArgumentParser(
        description="Rename AW139/FAST files for upload to RAISE platform. "
                    "Files have been converted to CSV by L3Harris")
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        default='',
        help="Path to input AW139 files",
        type=str
    )
    parser.add_argument(
        "-u",
        "--upload_path",
        required=True,
        default='',
        help="Path to renamed files, ready for upload.",
        type=str
    )
    args = parser.parse_args()
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    logging.info('parse_command_arguments: Input files path: %s', args.input_path)
    logging.info('parse_command_arguments: Upload files path: %s', args.upload_path)
    return args


def read_to_dataframe(path, file):
    new_df = pd.read_csv(os.path.join(path, file))
    return new_df.drop(index=0)


def read_MDY_HMS(flt_df):
    mo = flt_df['Month'][1]
    da = flt_df['Day'][1]
    ye = flt_df['Year'][1]
    ho = flt_df['Hour'][1]
    mi = flt_df['Minute'][1]
    se = flt_df['Second'][1]
    return mo, da, ye, ho, mi, se


def build_dt_string(mo, da, ye, ho, mi, se):
    ye_str = str(int(ye))
    mo_str = str(int(mo))
    if len(mo_str) == 1:
        mo_str = f'0{mo_str}'
    da_str = str(int(da))
    if len(da_str) == 1:
        da_str = f'0{da_str}'
    ho_str = str(int(ho))
    if len(ho_str) == 1:
        ho_str = f'0{ho_str}'
    mi_str = str(int(mi))
    if len(mi_str) == 1:
        mi_str = f'0{mi_str}'
    se_str = str(int(se))
    if len(se_str) == 1:
        se_str = f'0{se_str}'
    return f'{ye_str}{mo_str}{da_str}T{ho_str}{mi_str}{se_str}'


def l3h_133_rename_main(argv):
    """
    Renames AW139/FAST files that have been converted to CSV format for upload
    to RAISE.

    :param argv:
    :return:
    """
# def l3h_133_rename_main():

    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    logging.info('l3h_133_rename_main: Begin processing')

    command_line_arguments = parse_command_arguments(argv)
    path_139 = command_line_arguments.input_path
    path_upload = command_line_arguments.upload_path

    # path_139 = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/VMtools/139data"
    # path_upload = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/Flight_File_Handler/ASIAS_uploads"
    files_only = os.listdir(path_139)

    # file_139 = "PFI-AW139_N8CP_HPN_LOM_375245eaaf60_45774922_rotor_asias.csv"

    for file_139 in files_only:
        flight_df = read_to_dataframe(path_139, file_139)
        tail_num = file_139.split('_')[1]
        mon, day, year, hr, mi, sec = read_MDY_HMS(flight_df)
        dt_str = build_dt_string(mon, day, year, hr, mi, sec)
        new_filename = f'{tail_num}_{dt_str}_TD.csv'
        logging.info('l3h_133_rename_main: Renaming %s as %s', file_139, new_filename)
        if os.path.exists(path_139):
            try:
                os.rename(os.path.join(path_139, file_139),
                          os.path.join(path_upload, new_filename))
            except FileExistsError:
                logging.info('l3h_133_rename_main: EXCEPTION: file %s '
                             'already exists in %s', new_filename, path_upload)
        else:
            logging.info('l3h_133_rename_main: path %s does '
                         'not exist', path_139)


if __name__ == "__main__":
    l3h_133_rename_main(sys.argv[1:])
    # l3h_133_rename_main()



