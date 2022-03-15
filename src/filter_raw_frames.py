from src.frame_control_information import FrameControlInformation


class FilterFrameIterator:
    # Whitelist of frame types that are relevant
    whitelist = ['image', 'depth', 'pose', 'skeleton', 'skeleton_depth', 'skeleton_color']

    # Blacklist of frame types that are not relevant
    blacklist = []

    def filter_raw_frames(self, frames):
        """
            Return a iterator that passes frames that are relevant, based on the frame type
        :param frames:
        :return:
        """
        for frame in frames:
            # TODO only yield if match
            yield frame
