import os
import re
import shutil


def filter_by_date():
    path = 'C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/AGL/JAARS data/P2-SIR-20240102T190425Z-002/P2-SIR/2020 August 17 backup WO 20-027/data_log'
    dest = 'C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/AGL/'
    for f in os.listdir(path):
        if f[4:8] > '2010':
            shutil.move(os.path.join(path, f), os.path.join(dest, f))
            print(f'moving file {f} to {dest}')
        else:
            print(f'not moving file {f}')


if __name__ == '__main__':
    filter_by_date()
