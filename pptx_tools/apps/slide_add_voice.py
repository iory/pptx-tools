#!/usr/bin/env python

import argparse
from pathlib import Path

from eos import make_fancy_output_dir
import termcolor

from pptx_tools.utils import add_synthesize_audio


def main():
    parser = argparse.ArgumentParser(description='Add voice to presentation.')
    parser.add_argument("input", help="The input pptx file.")
    parser.add_argument("--out", help="The output dir of audio.",
                        default='./presentations')
    args = parser.parse_args()
    output_dir = Path(make_fancy_output_dir(
        args.out, no_save=True))
    output_slide_path = add_synthesize_audio(
        args.input, output_dir)
    termcolor.cprint('=> Saved to {}'.format(output_slide_path), 'green')


if __name__ == '__main__':
    main()
