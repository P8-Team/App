from expiringdict import ExpiringDict


def frame_aggregator(generator, threshold=None, max_age_seconds=None, max_buffer_size=None):
    """
    Generator that yields combined frames from a generator.
    If frames are equal, combine into one with multiple signal_strengths and sniff_timestamps.
    If some threshold of combined frames is reached, yield the combined frame.

    :param generator: generator that yields frames
    :param threshold: number of frames to combine before yielding
    :param max_age_seconds: max age of frames in buffer
    :param max_buffer_size: max number of frames in buffer
    :return: generator that yields combined frames
    """
    # TODO: Maybe add these to config?
    if threshold is None:
        threshold = 3
    if max_age_seconds is None:
        max_age_seconds = 2
    if max_buffer_size is None:
        max_buffer_size = 10000

    buffer = ExpiringDict(max_age_seconds=max_age_seconds, max_len=max_buffer_size)
    for frame in generator:
        # Create hash of frame
        frame_hash = hash(frame)
        buffer_frame = buffer.get(frame_hash)
        # Check if frame is in buffer
        if buffer_frame is not None:
            # Append signal_strength and sniff_timestamps to buffer_frame
            buffer_frame.wlan_radio.signals.append(frame.wlan_radio.signals[0])
        else:
            # Add frame to buffer
            buffer[frame_hash] = frame
            buffer_frame = frame
        # Check if threshold of combined frames is reached
        if len(buffer_frame.wlan_radio.signals) == threshold:
            buffer.pop(frame_hash)
            yield buffer_frame
