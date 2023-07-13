import os
import os.path as osp
from pathlib import Path
import tempfile
from zipfile import ZipFile

import skvideo.io

from pptx_tools.slide_info import get_slide_info


DEFAULT_PATH_PPT = 'ppt/media'
VIDEO_EXTENSIONS = ['mp4', 'avi', 'mpg', 'mpeg', 'wmv']


def get_video_duration(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    return float(metadata['video']['@duration'])


def add_video_duration(pptx_filename, infos):
    tmpdirname = tempfile.TemporaryDirectory()
    with ZipFile(pptx_filename, 'r') as zipObject:
        for filename in zipObject.namelist():
            if filename.startswith(DEFAULT_PATH_PPT):
                file_base_name, file_extension = os.path.splitext(filename)
                if file_extension[1:] in VIDEO_EXTENSIONS:
                    info = get_slide_info(file_base_name, infos)
                    slide_folder = Path(tmpdirname.name) \
                        / str(info['num_slide'])
                    slide_folder.mkdir(parents=True, exist_ok=True)
                    zipObject.extract(filename, slide_folder)
                    info['video_duration'] = get_video_duration(
                        slide_folder / filename)
    tmpdirname.cleanup()


def max_video_duration(slide_infos):
    video_durations = [info['video_duration'] for info in slide_infos
                       if 'video_duration' in info]
    if len(video_durations) > 0:
        return max(video_durations)
    else:
        return 0.0
