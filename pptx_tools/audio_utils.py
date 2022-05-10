import contextlib
import wave


def get_wave_duration(wave_filepath):
    with contextlib.closing(wave.open(str(wave_filepath), 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration
