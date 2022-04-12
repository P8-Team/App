class WifiCard:
    interface_name: str
    location: [float, float]

    def __init__(self, interface_name: str, location: [float, float]):
        self.interface_name = interface_name
        self.location = location
