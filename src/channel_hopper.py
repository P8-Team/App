from multiprocessing import Process, Value

import os
import time

# TODO: There might be a bug where after having run "sudo airmon-ng start <interface>", the interface drops back to
#  managed after some time. I haven't been able to reproduce it or force it.
#  Possible solution: Airmon says that there are some processes that might interfere and switch the interface back to
#  managed mode. It might be possible to kill those processes.

# TODO: This needs sudo or root access to work. That might be a problem?

# See which channels are available to it and which channel the interface is listening on: 'sudo iwlist <interface> channel'

# !!!Note: The interface has to be in monitor before!!!
# Change channel: 'sudo iwconfig <interface> channel <channel number>'


class ChannelHopper:
    process = None

    def __init__(self, wlan_interfaces, channels=None, sleep_time_sec=None):
        self.interfaces = wlan_interfaces
        if channels == None:
            self.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        else:
            self.channels = channels

        if sleep_time_sec == None:
            self.sleep_time_sec = 2
        else:
            self.sleep_time_sec = sleep_time_sec


    def start(self):
        print("Starting channel hopper")
        self.process = Process(target=self.hop, args=(self.interfaces, self.channels, self.sleep_time_sec))
        self.process.start()

    def stop(self):
        print("Stopping channel hopper")
        self.process.terminate()

    @staticmethod
    def hop(interfaces, channels, sleep_time):
        hop_command = 'sudo iwconfig {} channel {}'
        channel_index = 0
        while True:
            for interface in interfaces:
                os.system(hop_command.format(interface, channels[channel_index]))
                print(hop_command.format(interface, channels[channel_index]))

            channel_index = (channel_index + 1) % len(channels)
            time.sleep(sleep_time)


