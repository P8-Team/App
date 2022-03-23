from expiringdict import ExpiringDict


def frame_aggregator(generator, threshold=3, max_age_seconds=2, max_buffer_size=10000):
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
    buffer = ExpiringDict(max_age_seconds=max_age_seconds, max_len=max_buffer_size)
    for frame in generator:
        # Create hash of frame
        frame_hash = hash(frame)
        buffer_frame = buffer.get(frame_hash)
        # Check if frame is in buffer
        if buffer_frame is not None:
            # Append signal_strength and sniff_timestamps to buffer_frame
            buffer_frame.sniff_timestamp.append(frame.sniff_timestamp)
            buffer_frame.wlan_radio.signal_strength.append(frame.wlan_radio.signal_strength)
        else:
            # Add frame to buffer
            frame.sniff_timestamp = [frame.sniff_timestamp]
            frame.wlan_radio.signal_strength = [frame.wlan_radio.signal_strength]
            buffer[frame_hash] = frame
            buffer_frame = frame
        # Check if threshold of combined frames is reached
        if len(buffer_frame.sniff_timestamp) == threshold or len(buffer_frame.wlan_radio.signal_strength) == threshold:
            buffer.pop(frame_hash)
            yield buffer_frame
