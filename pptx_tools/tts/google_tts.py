from pathlib import Path

from google.cloud import texttospeech
import pydub

from .google_tts_voice import voice_name_to_language_code


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

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(
        text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        sample_rate_hertz=sample_rate,
        speaking_rate=speaking_rate)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config)

    with open(str(audio_filepath.with_suffix('.mp3')), 'wb') as out:
        out.write(response.audio_content)

    if audio_filepath.suffix == '.wav':
        sound = pydub.AudioSegment.from_mp3(
            str(audio_filepath.with_suffix('.mp3')))
        sound.export(str(audio_filepath), format="wav")
