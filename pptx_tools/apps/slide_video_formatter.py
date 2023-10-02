#!/usr/bin/env python

import argparse
import sys

import termcolor

from pptx_tools.video_utils import exist_ffmpeg
from pptx_tools.video_utils import format_pptx_video


def main():
    parser = argparse.ArgumentParser(description='Format slide video.')
    parser.add_argument("input", help="The input pptx file.")
    parser.add_argument("--out", help="The output pptx filename.",
                        default='')
    parser.add_argument('--vcodec', type=str, default='libx264',
                        help='Video codec to use')
    parser.add_argument('--pix-fmt', type=str, default='yuv420p',
                        help='Pixel format to use')
    parser.add_argument('--audio-bitrate', type=str, default='128k',
                        help='Audio bitrate to use')
    parser.add_argument('--crf', type=int, default=28, help='CRF value to use')
    args = parser.parse_args()
    if len(args.out) == 0:
        args.out = args.input
    if exist_ffmpeg() is False:
        termcolor.cprint("ffmpeg is not installed. Please install it.", 'red')
        sys.exit(1)
    format_pptx_video(args.input, args.out,
                      vcodec=args.vcodec,
                      pix_fmt=args.pix_fmt, crf=args.crf,
                      audio_bitrate=args.audio_bitrate)
    termcolor.cprint('=> Saved to {}'.format(args.out), 'green')


if __name__ == '__main__':
    main()
