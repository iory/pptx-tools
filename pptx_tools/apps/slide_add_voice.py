#!/usr/bin/env python

import argparse
from pathlib import Path
import sys

from eos import make_fancy_output_dir
import termcolor

from pptx_tools.utils import add_synthesize_audio
from pptx_tools.video_utils import exist_ffmpeg


def main():
    tts_engines = ['google', 'azure']
    parser = argparse.ArgumentParser(description='Add voice to presentation.')
    parser.add_argument("input", help="The input pptx file.")
    parser.add_argument("--out", help="The output dir of audio.",
                        default='./presentations')
    parser.add_argument("--voice-name", type=str,
                        help='If not set, use default value.')
    parser.add_argument("--tts", choices=tts_engines,
                        default='google',
                        help='select the text-to-speech engine. '
                        'You can choose {}.'.format(tts_engines))
    parser.add_argument("--slide-duration-offset", type=float,
                        default=1.0)
    args = parser.parse_args()
    if exist_ffmpeg() is False:
        termcolor.cprint("ffmpeg is not installed. Please install it.", 'red')
        sys.exit(1)
    if args.voice_name is not None:
        if args.tts == 'google':
            from pptx_tools.tts.google_tts_voice import \
                voice_name_to_language_code as google_voice
            if args.voice_name not in google_voice:
                print('Invalid voice_name. Avaliable voices are:')
                print([voice for voice in google_voice.keys()])
                print("You can check the sample audio here: "
                      "https://cloud.google.com/text-to-speech/docs/voices")
                sys.exit(0)
        elif args.tts == 'azure':
            from pptx_tools.tts.azure_tts_voice import \
                voice_name_to_language_code as azure_voice
            if args.voice_name not in azure_voice:
                print('Invalid voice_name. Avaliable voices are:')
                print([voice for voice in azure_voice.keys()])
                sys.exit(0)
    output_dir = Path(make_fancy_output_dir(
        args.out, no_save=True))
    output_slide_path = add_synthesize_audio(
        args.input, output_dir, voice_name=args.voice_name,
        slide_duration_offset=args.slide_duration_offset)
    termcolor.cprint('=> Saved to {}'.format(output_slide_path), 'green')


if __name__ == '__main__':
    main()
