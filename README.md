# pptx-tools

[![Build Status](https://github.com/iory/pptx-tools/workflows/Run%20Tests/badge.svg?branch=master)](https://github.com/iory/pptx-tools/actions)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![](https://badge.fury.io/py/pptx-tools.svg)](https://pypi.org/project/pptx-tools/)

## Install

Suport only python3.

```
pip install pptx-tools
```

## Quick Example

Create Google Application Credentials files and set

```
export GOOGLE_APPLICATION_CREDENTIALS=/PATH/TO/JSON
```

After that,

```
slide-add-voice <PATH-TO-YOUR-AWESOME-SLIDE>
```

You can change the synthesized voice by specifying the `--voice-name` as shown below.

```
slide-add-voice pptx_tools/data/hello.pptx --voice-name en-US-Wavenet-C
```

In addition, you can listen to the voice samples available for use with Google Text-to-Speech at the following URL: https://cloud.google.com/text-to-speech/docs/voices

## Q & A

Q: What happens to the slide transition time when both a video file and a synthesized voice are present on the slide?

A: The transition time for the slide will be based on whichever is longer between the duration of the synthesized voice and the duration of the video.
