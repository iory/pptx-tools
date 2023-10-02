import os
import os.path as osp
from pathlib import Path
import shutil
import tempfile
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import skvideo
import skvideo.io

from pptx_tools.slide_info import get_slide_info
from pptx_tools.subprocess_utils import run_command


DEFAULT_PATH_PPT = 'ppt/media'
VIDEO_EXTENSIONS = ['mp4', 'avi', 'mpg', 'mpeg', 'wmv']


def exist_ffmpeg():
    return len(skvideo.which('ffmpeg')) != 0


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


def convert_video(video_path, ffmpeg_params):
    path = Path(video_path)
    with tempfile.TemporaryDirectory() as tmpdir:
        dst_path = Path(tmpdir) / path.with_suffix('.mp4').name
        cmd = 'ffmpeg -i "{}" -vcodec {} -pix_fmt {} -c:a aac -strict experimental -b:a {} -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -crf "{}" "{}"'.format(  # NOQA
            path, ffmpeg_params['vcodec'], ffmpeg_params['pix_fmt'], ffmpeg_params['audio_bitrate'], ffmpeg_params['crf'], dst_path)  # NOQA
        run_command(cmd, shell=True)
        shutil.copy(dst_path, path.with_suffix('.mp4'))


def convert_target(file_path, old_target, new_target):
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {'rels':
          'http://schemas.openxmlformats.org/package/2006/relationships'}
    for relationship in root.findall('rels:Relationship', ns):
        if relationship.get('Target') == old_target:
            relationship.set('Target', new_target)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


def format_pptx_video(pptx_filename, output_pptx_filename=None,
                      vcodec='libx264', crf=28,
                      pix_fmt='yuv420p', audio_bitrate='128k'):
    ffmpeg_params = {'vcodec': vcodec, 'pix_fmt': pix_fmt,
                     'audio_bitrate': audio_bitrate, 'crf': crf}

    extracted_dir = tempfile.TemporaryDirectory()
    with ZipFile(pptx_filename, 'r') as zip_ref:
        zip_ref.extractall(extracted_dir.name)

    temp_zip_name = tempfile.mktemp(suffix='.zip')
    names = []
    for foldername, subfolders, filenames in os.walk(extracted_dir.name):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            file_base_name, file_extension = os.path.splitext(filename)
            if file_extension[1:].lower() in VIDEO_EXTENSIONS:
                file_path = os.path.join(
                    foldername, "{}.mp4".format(file_base_name))
                names.append(('../media/{}'.format(filename),
                              "../media/{}.mp4".format(file_base_name)))
            arcname = os.path.relpath(file_path, extracted_dir.name)

    for frm, to in names:
        for xml_path in (Path(
                extracted_dir.name) / 'ppt/slides/_rels/').glob(
                    'slide*.xml.rels'):
            convert_target(xml_path, frm, to)

    with ZipFile(temp_zip_name, 'w') as new_zip:
        for foldername, subfolders, filenames in os.walk(extracted_dir.name):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                file_base_name, file_extension = os.path.splitext(filename)
                if file_extension[1:].lower() in VIDEO_EXTENSIONS:
                    convert_video(file_path, ffmpeg_params)
                    file_path = os.path.join(
                        foldername, "{}.mp4".format(file_base_name))
                    names.append(('../media/{}'.format(filename),
                                  "../media/{}.mp4".format(file_base_name)))
                arcname = os.path.relpath(file_path, extracted_dir.name)
                new_zip.write(file_path, arcname)

    extracted_dir.cleanup()
    if output_pptx_filename is None:
        output_pptx_filename = pptx_filename
    shutil.copy(temp_zip_name, output_pptx_filename)
