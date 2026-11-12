from io import BytesIO
from pathlib import Path

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine


def test_resizing_transparent_palette_gif_preserves_transparency():
    source_path = (
        Path(__file__).resolve().parents[1] / "course" / "images" / "sticker.gif"
    )
    engine = Engine(Context(config=Config()))
    engine.load(source_path.read_bytes(), ".gif")

    engine.resize(240, 160)

    output = Image.open(BytesIO(engine.read(".gif")))
    alpha = output.convert("RGBA").getchannel("A")

    assert output.info.get("transparency") is not None
    assert alpha.getextrema() == (0, 255)


def test_resizing_opaque_gif_does_not_add_transparency():
    source = BytesIO()
    Image.new("RGB", (20, 20), (255, 0, 0)).save(source, format="GIF")

    engine = Engine(Context(config=Config()))
    engine.load(source.getvalue(), ".gif")
    engine.resize(40, 40)

    output = Image.open(BytesIO(engine.read(".gif")))

    assert output.info.get("transparency") is None
    assert output.convert("RGBA").getchannel("A").getextrema() == (255, 255)
