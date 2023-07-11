# pptx-tools

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
