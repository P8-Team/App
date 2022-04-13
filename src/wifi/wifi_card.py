from sympy import Point2D


class WifiCard:
    interface_name: str
    location: Point2D

    def __init__(self, interface_name: str, location: Point2D):
        self.interface_name = interface_name
        self.location = location

    def __repr__(self) -> str:
        return f"WifiCard(interface_name={self.interface_name}, location={self.location})"
