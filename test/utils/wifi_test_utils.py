class Layer:
    def __init__(self, attribute_dict):
        self.dict = attribute_dict

    def get(self, key):
        # If they key doesn't exist, return None
        if key not in self.dict:
            return None
        return self.dict[key]


class Frame:
    def __init__(self, length, sniff_timestamp, layer_dict):
        self.length = length
        self.sniff_timestamp = sniff_timestamp
        self.layers = layer_dict

    def __getattr__(self, key):
        return self.layers[key]
