class FrameFilter:

    def __init__(self, whitelisted_types=None, whitelisted_subtypes=None):
        # https://en.wikipedia.org/wiki/802.11_Frame_Types
        if whitelisted_types is None:
            whitelisted_types = [2]
        if whitelisted_subtypes is None:
            whitelisted_subtypes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.whitelisted_types = whitelisted_types
        self.whitelisted_subtypes = whitelisted_subtypes

    def filter(self, generator):
        """
            Filters the generator for types/subtypes not in whitelist.
        :param generator:
        :return:
        """
        return FrameFilter.filter_generator(generator,
                                            lambda frame:
                                            self.filter_frames_by_subtypes(frame, self.whitelisted_subtypes)
                                            and self.filter_frames_by_types(frame, self.whitelisted_types)
                                            )

    @staticmethod
    def filter_generator(generator, filter_func):
        """
            Filters a frame generator using a filter function.
        :param generator:
        :param filter_func:
        :return:
        """
        for frame in generator:
            if filter_func(frame):
                yield frame

    @staticmethod
    def filter_frames_by_types(frame, types):
        return frame.frame_control_information.type in types

    @staticmethod
    def filter_frames_by_subtypes(frame, subtypes):
        return frame.frame_control_information.subtype in subtypes
