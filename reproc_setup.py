import pandas as pd
import os
import shutil

# read CSV of Polaris processed files to dataframes
segments_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/VMtools/RLC_reprocess"
segments_file = 'segment_search.csv'
segments_df = pd.read_csv(os.path.join(segments_path, segments_file))
print(f'processing files from {segments_file}')

# polaris_file = "/mnt/analysis/188/568/633/2/RLC_VIRTUAL_N669RL_20231107022359_00_APPAREO__1923_VISFK4M__convertedVISFK4M04257csv.dat.001.hdf5"
# polaris_file = "/mnt/analysis/188/568/633/2/RLC_VIRTUAL_N669RL_20231107022359_00_APPAREO__1923_VISFK4M__convertedVIS12345604257csv.dat.001.hdf5"

match_str_list = []
for index, row in segments_df.iterrows():
    # parse psuedo filenames and add as new column ("Reprocess")
    polaris_file = row['File']
    polaris_file_splitlist = polaris_file.split('_')
    temp_name = polaris_file_splitlist[10]
    temp_name_splitlist = temp_name.split('.')
    pseudo_name = temp_name_splitlist[0]
    converted_removed = pseudo_name[9:]
    vis_removed = converted_removed[3:]
    csv_removed = vis_removed[:-3]
    core_name = vis_removed[:-3]

    if len(core_name) == 9:  # if 9 chars, V1000
        match_str = core_name[:4] + '-' + core_name[4:]
    elif len(core_name) == 11:  # if 11 chars, AIRS400
        match_str = core_name[:6] + '-' + core_name[6:]
    else:
        match_str = 'None'

    match_str_list.append(match_str)
    print(match_str)

# get the list of archived files (Z)
archive_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/VMtools/RLC_reprocess/archive"
files_only = os.listdir(archive_path)

# search for match strings in archive list, on match add to list
recover_list = []
for f in files_only:
    for match in match_str_list:
        if match in f:
            recover_list.append(f)

print(f'Files matched: {len(recover_list)}')

# copy matched files in list to F drive
temp_path = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/VMtools/RLC_reprocess/temp"
for f in recover_list:
    shutil.copy(os.path.join(archive_path, f), os.path.join(temp_path, f))
    print(f'Copying file {f} from archive to temp dir')

print(f'Files copied: {len(recover_list)}')
print(f'processing complete for {segments_file}')

