from __future__ import print_function

import os
import shlex
import subprocess
import sys

from setuptools import find_packages
from setuptools import setup


version = "0.1.9"


def git(*args):
    return subprocess.check_call(['git'] + list(args))


def check_if_tag_exists(version):
    try:
        git("rev-parse", "v{:s}".format(version))
        return True
    except subprocess.CalledProcessError:
        return False


def push_tag(version):
    commands = []

    if not check_if_tag_exists(version):
        commands.append('git tag v{:s}'.format(version))
        commands.append('git push origin master --force --tags')

    for cmd in commands:
        print('+ {}'.format(cmd))
        subprocess.check_call(shlex.split(cmd))


if sys.argv[-1] == "release":
    # Release via github-actions.
    push_tag(version)
    sys.exit(0)


def listup_package_data():
    data_files = []
    for root, _, files in os.walk('pptx_tools/data'):
        for filename in files:
            data_files.append(
                os.path.join(
                    root[len('pptx_tools/'):],
                    filename))
    return data_files


setup_requires = []

with open('requirements.txt') as f:
    install_requires = []
    for line in f:
        req = line.split('#')[0].strip()
        install_requires.append(req)

azure_install_requires = []
with open('requirements_azure.txt') as f:
    azure_install_requires = []
    for line in f:
        req = line.split('#')[0].strip()
        azure_install_requires.append(req)

setup(
    name="pptx-tools",
    version=version,
    description="A power point tools",
    author="iory",
    author_email="ab.ioryz@gmail.com",
    url="https://github.com/iory/pptx-tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=find_packages(),
    package_data={'pptx_tools': listup_package_data()},
    zip_safe=False,
    setup_requires=setup_requires,
    install_requires=install_requires,
    extras_require={
        'azure': azure_install_requires,
        'all': (install_requires
                + azure_install_requires),
    },
    entry_points={
        "console_scripts": [
            "slide-add-voice=pptx_tools.apps.slide_add_voice:main",
            "slide-delete-notes=pptx_tools.apps.slide_delete_notes:main",
            "slide-manual-transition\
             =pptx_tools.apps.slide_manual_transition:main",
            "slide-check-fonts=pptx_tools.apps.slide_check_fonts:main",
            "slide-video-formatter=pptx_tools.apps.slide_video_formatter:main"
        ]
    },
)
