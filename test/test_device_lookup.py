import pytest
import pandas as pd
from src.device_lookup import DeviceLookup


def test_data_is_loaded():
    dl = DeviceLookup()
    assert dl.lookup_data is not None
    assert type(dl.lookup_data) is pd.DataFrame
    assert dl.lookup_data.empty is False


def test_find_selected_data():
    dl = DeviceLookup()
    test_data = pd.read_csv(r'..\Data\test_data.csv', index_col=['Labels'])
    dl.lookup_data = pd.DataFrame(test_data)

    assert dl.all_mac_addresses() == ['42:R2:D2:C3:PO:42', 'A1:B2:C3:D4:E5:F6']
    assert dl.lookup_device_by_label('LargeOrc') == [-20, '42:R2:D2:C3:PO:42', 'Limited Edition Thrall Camera']
    assert dl.lookup_device_by_label('Wink') == [-10, 'A1:B2:C3:D4:E5:F6', 'Totally Not a Cam Camera']


