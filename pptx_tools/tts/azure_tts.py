import os

from azure.cognitiveservices.speech.audio import AudioOutputConfig
from azure.cognitiveservices.speech import SpeechConfig
from azure.cognitiveservices.speech import SpeechSynthesizer

from .azure_tts_voice import voice_name_to_language_code


lower2original = {k.lower(): k
                  for k in voice_name_to_language_code}


def determine_voice_name(voice_name):
    voice_name = voice_name.lower()
    if len(voice_name) == 0:
        name = 'en-US-BrandonNeural'
        language_code = 'en-US'
    else:
        candidates = list(filter(
            lambda lower_name: lower_name.startswith(voice_name),
            lower2original))
        if candidates:
            wavenet_candidates = list(
                filter(lambda c: 'wavenet' in c, candidates))
            voice_name = wavenet_candidates[0] \
                if wavenet_candidates else candidates[0]
            name = lower2original[voice_name]
            language_code = voice_name_to_language_code[name]
        else:
            raise RuntimeError('[Text2Wave] Invalid voice_name ({})'.format(
                voice_name))
    return name, language_code


def azure_text_to_speech(audio_filepath, text,
                         voice_name='en-US-BrandonNeural',
                         azure_key=None,
                         azure_region=None):
    audio_filepath = str(audio_filepath)
    if azure_key is None:
        azure_key = os.environ.get('AZURE_KEY', None)
        if azure_key is None:
            raise RuntimeError('AZURE_KEY is not specified.')
        azure_region = os.environ.get('AZURE_REGION', None)
        if azure_region is None:
            raise RuntimeError('AZURE_REGION is not specified.')
    voice_name, language_code = determine_voice_name(voice_name)

    speech_config = SpeechConfig(subscription=azure_key,
                                 region=azure_region)
    speech_config.speech_synthesis_voice_name = voice_name
    speech_config.request_word_level_timestamps()
    speech_config.speech_recognition_language = language_code

    audio_config = AudioOutputConfig(filename=audio_filepath)
    synthesizer = SpeechSynthesizer(speech_config=speech_config,
                                    audio_config=audio_config)
    synthesizer.speak_text_async(text)
