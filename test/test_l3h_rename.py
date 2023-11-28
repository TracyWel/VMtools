import pytest

from l3h_139_rename import read_to_dataframe, read_MDY_HMS, \
    build_dt_string


def test_read_to_dataframe():
    path_139 = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/VMtools/139data"
    file_139 = "PFI-AW139_N8CP_HPN_LOM_375245eaaf60_45774922_rotor_asias.csv"
    flight_df = read_to_dataframe(path_139, file_139)
    print(f'\n{flight_df.head()}')
    assert(flight_df['Month'][1] == 10.0)

def test_read_MDY_HMS():
    path_139 = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/VMtools/139data"
    file_139 = "PFI-AW139_N8CP_HPN_LOM_375245eaaf60_45774922_rotor_asias.csv"
    flight_df = read_to_dataframe(path_139, file_139)
    mon, day, year, hr, mi, sec = read_MDY_HMS(flight_df)
    assert(mon == 10.0)


def test_build_dt_str():
    path_139 = "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/VMtools/139data"
    file_139 = "PFI-AW139_N8CP_HPN_LOM_375245eaaf60_45774922_rotor_asias.csv"
    flight_df = read_to_dataframe(path_139, file_139)
    mon, day, year, hr, mi, sec = read_MDY_HMS(flight_df)
    dt_str = build_dt_string(mon, day, year, hr, mi, sec)
    assert dt_str == '20231003T125611'
