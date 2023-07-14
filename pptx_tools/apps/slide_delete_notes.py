#!/usr/bin/env python

import argparse

import termcolor

from pptx_tools.utils import delete_slide_notes_text


def main():
    parser = argparse.ArgumentParser(description='Delete slide notes text.')
    parser.add_argument("input", help="The input pptx file.")
    parser.add_argument("--out", help="The output filename of slide.",
                        required=True)
    args = parser.parse_args()

    termcolor.cprint('Delete slide notes', 'green')
    presentation = delete_slide_notes_text(args.input)
    presentation.save(args.out)
    termcolor.cprint('=> Saved to {}'.format(args.out), 'green')


if __name__ == '__main__':
    main()
