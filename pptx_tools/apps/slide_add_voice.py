#!/usr/bin/env python

import argparse
from pathlib import Path

from eos import make_fancy_output_dir

from pptx_tools.utils import synthesize_audio_azure


def main():
    parser = argparse.ArgumentParser(description='Add voice to presentation.')
    parser.add_argument("input", help="The input pptx file.")
    parser.add_argument("--out", help="The output dir of audio.",
                        default='./presentations')
    args = parser.parse_args()
    output_dir = Path(make_fancy_output_dir(
        args.out, no_save=True))
    synthesize_audio_azure(
        args.input, output_dir)


if __name__ == '__main__':
    main()
