import os
import shutil
import subprocess
import tempfile
import unittest

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
        if proc.returncode != 0:
            raise RuntimeError

        # clean test directory
        shutil.rmtree(dirname)
