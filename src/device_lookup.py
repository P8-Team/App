import pandas as pd


class DeviceLookup:

    def __init__(self):
        self.lookup_data = pd.read_csv(r'..\Data\hard_data.csv', index_col=['Labels'])

    def print_data(self):
        print(self.lookup_data)

    def lookup_device_by_label(self, label):
        # Returns a list with transmission power, mac address and device name for a given label
        return self.lookup_data.loc[label].values.tolist()

    def all_mac_addresses(self):
        # Returns a list all mac addresses, representing all the devices we can identify
        return self.lookup_data['Mac Address'].values.tolist()

