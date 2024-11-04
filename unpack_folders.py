import os
import shutil
import sys


def unpack_data_folders():
    source_folder = 'C:/Users/TracyTD/Downloads/JAARsKodiakdata/JAARsKodiakdata'
    destination_folder = 'C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/AGL/AGL/data_source'
    print(f'moving all files under {source_folder} to {destination_folder}')
    response = input('ok? (Y or N)')
    if 'N' in response.upper():
        sys.exit(-1)

    assert os.path.isdir(source_folder)

    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            print(f'moving file: {file_name}')
            shutil.move(os.path.join(root, file_name),
                        os.path.join(destination_folder, file_name))


if __name__ == '__main__':
    unpack_data_folders()
