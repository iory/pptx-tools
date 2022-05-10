from pathlib import Path


data_dir = Path(__file__).resolve().parent


def get_transparent_img_path():
    return data_dir / 'transparent.png'


def get_hello_pptx_path():
    return data_dir / 'hello.pptx'
