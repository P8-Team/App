from multiprocessing import Process

import os
import time

# TODO: There might be a bug where after having run "sudo airmon-ng start <interface>", the interface drops back to
#  managed after some time. I haven't been able to reproduce it or force it.
#  Possible solution: Airmon says that there are some processes that might interfere and switch the interface back to
#  managed mode. It might be possible to kill those processes (without killing SSH access).

# TODO: This needs sudo or root access to work. That might be a problem?

# See which channels are available and which channel the interface is listening on: 'sudo iwlist <interface> channel'

# !!!Note: The interface has to be in monitor before!!!
# Change channel: 'sudo iwconfig <interface> channel <channel number>'
# or 'sudo iw dev <interface> set channel <channel number>'


class ChannelHopper:
    channels = [1, 2, 3]
    sleep_time_sec = 1

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
        command = 'sudo iw dev {} set channel {}'
        index = 0
        while True:
            for interface in self.interfaces:
                os.system(command.format(interface, self.channels[index]))
                print(command.format(interface, self.channels[index]))

            index = (index + 1) % len(self.channels)
            time.sleep(self.sleep_time_sec)


