#!/usr/bin/env python

import argparse

import termcolor

from pptx_tools.utils import manual_transition


def main():
    parser = argparse.ArgumentParser(description='Delete slide transition.')
    parser.add_argument("input", help="The input pptx file.")
    parser.add_argument("--out", help="The output filename of slide.",
                        required=True)
    args = parser.parse_args()

    termcolor.cprint('Delete slide transition', 'green')
    presentation = manual_transition(args.input)
    presentation.save(args.out)
    termcolor.cprint('=> Saved to {}'.format(args.out), 'green')


if __name__ == '__main__':
    main()
