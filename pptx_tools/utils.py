from pathlib import Path

from eos import makedirs
from lxml import etree
from pptx import Presentation
from pptx.util import Inches
from pybsc.audio_utils import get_wave_duration
from pybsc.tts import azure_text_to_speech

from pptx_tools.data import get_transparent_img_path


def xpath(el, query):
    nsmap = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
    return etree.ElementBase.xpath(el, query, namespaces=nsmap)


def autoplay_media(media):
    el_id = xpath(media.element, './/p:cNvPr')[0].attrib['id']
    el_cnt = xpath(
        media.element.getparent().getparent().getparent(),
        './/p:timing//p:video//p:spTgt[@spid="%s"]' % el_id,
    )[0]
    cond = xpath(el_cnt.getparent().getparent(), './/p:cond')[0]
    cond.set('delay', '0')


def synthesize_audio_azure(input, outdir):
    """Synthesizes speech from the pptx."""

    output_path = Path(outdir)
    makedirs(output_path)

    presentation = Presentation(input)
    total_time = 0.0
    for page, slide in enumerate(presentation.slides, start=1):
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame.text:
            note_txt = slide.notes_slide.notes_text_frame.text
            note_txt = note_txt.replace('\n', ' ')
            wave_path = output_path / f'{page}.wav'
            azure_text_to_speech(wave_path, note_txt)
            total_time += get_wave_duration(wave_path)
            try:
                movie = slide.shapes.add_movie(
                    str(wave_path),
                    Inches(0), Inches(0), Inches(1.0), Inches(1.0),
                    poster_frame_image=str(get_transparent_img_path()),
                    mime_type='audio/wav')
            except AttributeError:
                print('Skip {}'.format(page))
                continue
            autoplay_media(movie)
    print('Total sound time: {}'.format(total_time))
    presentation.save(output_path / Path(input).name)
