

class WLANInterface:

    def __init__(self, interface):

        self.interface = interface
        self.current_channel = self.get_current_channel()

    def get_current_channel(self):
        return 1

    def set_current_channel(self, channel):
        return 1