from multiprocessing import Process

import os
import time


class ChannelHopper:
    channels = [1, 2, 3]
    sleep_time_sec = 10

    def __init__(self, wlan_interfaces):
        self.interfaces = wlan_interfaces

    def start(self):

        # pid = os.fork()
        #
        # # Parent can go back to do its thing
        # if pid > 0:
        #     return
        #
        # # Child continues with channel hopping
        # self.hop()

        p = Process(target=self.hop)
        p.start()

    def hop(self):
        command = 'iw dev {} set channel {}'
        index = 0
        while True:
            for interface in self.interfaces:
                # os.system(command.format(interface, self.channels[index]))
                print(command.format(interface, self.channels[index]))
                # yield command.format(interface, self.channels[index])

            index = (index + 1) % len(self.channels)
            time.sleep(self.sleep_time_sec)