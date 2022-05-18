import os.path

import pandas as pd


class DeviceLookup:

    def __init__(self, filepath):
        path_label_device_map = os.path.normpath(filepath)
        self.lookup_data = pd.read_csv(r'{}'.format(path_label_device_map), index_col=['Labels'])

    def print_data(self):
        print(self.lookup_data)

    def get_transmission_power_by_label(self, label):
        return self.get_device_info_by_label(label)[0]

    def get_device_info_by_label(self, label):
        # Returns a list with transmission power and device name for a given label
        return self.lookup_data.loc[label].values.tolist()

    def all_mac_addresses(self):
        # Returns a list all mac addresses, representing all the devices we can identify
        return self.lookup_data['Mac Address'].values.tolist()
