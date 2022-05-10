import os
import os.path as osp
import shutil
import tempfile
import unittest
import subprocess

from eos import makedirs

from pptx_tools.data import get_hello_pptx_path


class TestSlideAddVoice(unittest.TestCase):

    def test_command(self):
        # create test directory
        _, dirname = tempfile.mkstemp()
        os.remove(dirname)
        makedirs(dirname)

        slide_path = get_hello_pptx_path()
        cmd = 'slide-add-voice {} --out {}'.format(slide_path,
                                                   dirname)
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()

        # clean test directory
        shutil.rmtree(dirname)
