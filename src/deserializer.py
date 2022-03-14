from src.Packet import *


def parser(message: str):
    objects = list()
    parsed_elements = message.split(';')
    for elem in parsed_elements:
        if len(elem) > 0:
            current_element = elem.split(",")
            if len(current_element) < 3:
                raise TypeError("Not all fields are present.")
            objects.append(Packet(current_element[0], current_element[1], current_element[2]))
    return objects
