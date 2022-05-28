from distutils.version import LooseVersion
from pathlib import Path

from google.cloud.texttospeech import TextToSpeechClient
import pkg_resources
import pydub

from .google_tts_voice import voice_name_to_language_code


texttospeech_version = pkg_resources.get_distribution(
    "google-cloud-texttospeech").version
if LooseVersion(texttospeech_version) >= LooseVersion('2.0.0'):
    from google.cloud.texttospeech import AudioConfig
    from google.cloud.texttospeech import AudioEncoding
    from google.cloud.texttospeech import SsmlVoiceGender
    from google.cloud.texttospeech import SynthesisInput
    from google.cloud.texttospeech import VoiceSelectionParams
else:
    from google.cloud.texttospeech_v1.gapic.enums import AudioEncoding
    from google.cloud.texttospeech_v1.gapic.enums import SsmlVoiceGender
    from google.cloud.texttospeech_v1.types import AudioConfig
    from google.cloud.texttospeech_v1.types import SynthesisInput
    from google.cloud.texttospeech_v1.types import VoiceSelectionParams


lower2original = {k.lower(): k
                  for k in voice_name_to_language_code}


def determine_voice_name(voice_name):
    voice_name = voice_name.lower()
    if len(voice_name) == 0:
        name = 'en-US-Wavenet-A'
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


def google_text_to_speech(
        audio_filepath, text,
        voice_name='en-US-Wavenet-F',
        speaking_rate=1.0,
        sample_rate=16000):
    """Text to speech.

    You can see which language is available here
    https://cloud.google.com/text-to-speech/docs/voices
    """
    audio_filepath = Path(audio_filepath)
    voice_name, language_code = determine_voice_name(voice_name)

    client = TextToSpeechClient()

    synthesis_input = SynthesisInput(text=text)
    voice = VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = AudioConfig(
        audio_encoding=AudioEncoding.MP3,
        sample_rate_hertz=sample_rate,
        speaking_rate=speaking_rate)

    if LooseVersion(texttospeech_version) >= LooseVersion('2.0.0'):
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config)
    else:
        response = client.synthesize_speech(
            synthesis_input, voice, audio_config)

    with open(str(audio_filepath.with_suffix('.mp3')), 'wb') as out:
        out.write(response.audio_content)

    if audio_filepath.suffix == '.wav':
        sound = pydub.AudioSegment.from_mp3(
            str(audio_filepath.with_suffix('.mp3')))
        sound.export(str(audio_filepath), format="wav")
