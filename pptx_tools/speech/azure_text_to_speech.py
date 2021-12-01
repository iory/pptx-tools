import os

from azure.cognitiveservices.speech.audio import AudioOutputConfig
from azure.cognitiveservices.speech import SpeechConfig
from azure.cognitiveservices.speech import SpeechSynthesizer


def azure_text_to_speech(audio_filepath, text, azure_key=None,
                         azure_region=None,
                         locale='en-US'):
    audio_filepath = str(audio_filepath)
    if azure_key is None:
        azure_key = os.environ.get('AZURE_KEY', None)
        if azure_key is None:
            raise RuntimeError('AZURE_KEY is not specified.')
        azure_region = os.environ.get('AZURE_REGION', None)
        if azure_region is None:
            raise RuntimeError('AZURE_REGION is not specified.')

    speech_config = SpeechConfig(subscription=azure_key,
                                 region=azure_region)
    speech_config.speech_synthesis_voice_name = 'en-US-BrandonNeural'
    speech_config.request_word_level_timestamps()
    speech_config.speech_recognition_language = locale

    audio_config = AudioOutputConfig(filename=audio_filepath)
    synthesizer = SpeechSynthesizer(speech_config=speech_config,
                                    audio_config=audio_config)
    synthesizer.speak_text_async(text)
