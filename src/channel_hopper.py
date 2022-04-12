from multiprocessing import Process, Value

import os
import time


# TODO: Integrate the channel hopper into main.py

# TODO: This needs sudo or root access to work. That might be a problem when used with everything else?

# TODO: There might be a bug where after having run "sudo airmon-ng start <interface>", the interface drops back to
#  managed after some time. I haven't been able to reproduce it or force it.
#  Possible solution: Airmon says that there are some processes that might interfere and switch the interface back to
#  managed mode. It might be possible to kill those processes and solve this issue.


class ChannelHopper:
    hopper_process = None
    test_mode = False

    def __init__(self, wlan_interfaces, channels=None, time_between_hops_sec=None):
        if channels is None:
            channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        if time_between_hops_sec is None:
            time_between_hops_sec = 2

        self.interfaces = wlan_interfaces
        self.channels = channels
        self.sleep_time = time_between_hops_sec

    def start(self):
        print("Starting channel hopper")
        self.hopper_process = Process(target=self.__hop__, args=(self.interfaces, self.channels, self.sleep_time, self.test_mode))
        self.hopper_process.start()

    def stop(self):
        print("Stopping channel hopper")
        self.hopper_process.kill()

    @staticmethod
    def __hop__(interfaces, channels, sleep_time, test_mode):
        # The command for making an interface listen on a specified channel
        hop_command = 'sudo iwconfig {} channel {}'
        channel_index = 0
        while True:
            for interface in interfaces:
                if not test_mode:
                    os.system(hop_command.format(interface, channels[channel_index]))
                print("{}: channel {}".format(interface, channels[channel_index]))

            # Switch to the next channel for next round
            channel_index = (channel_index + 1) % len(channels)
            time.sleep(sleep_time)
