import os.path

import pandas as pd

from src.device_lookup import DeviceLookup


def test_data_is_loaded():
    dl = DeviceLookup('Data/label_device_maps/label_device_map.csv')
    assert dl.lookup_data is not None
    assert type(dl.lookup_data) is pd.DataFrame
    assert dl.lookup_data.empty is False


def test_find_selected_data():
    dl = DeviceLookup('Data/label_device_maps/label_device_map.csv')
    path_test_data = os.path.normpath('test/test_data/device_data.csv')
    test_data = pd.read_csv(r'{}'.format(path_test_data), index_col=['Labels'])
    dl.lookup_data = pd.DataFrame(test_data)

    assert dl.all_mac_addresses() == ['42:R2:D2:C3:PO:42', 'A1:B2:C3:D4:E5:F6']
    assert dl.get_device_info_by_label('LargeOrc') == [-20, '42:R2:D2:C3:PO:42', 'Limited Edition Thrall Camera']
    assert dl.get_transmission_power_by_label('LargeOrc') == -20
    assert dl.get_device_info_by_label('Wink') == [-10, 'A1:B2:C3:D4:E5:F6', 'Totally Not a Cam Camera']
    assert dl.get_transmission_power_by_label('Wink') == -10
