"""
The 'font' module defines the 'Font' class and defines the 'default_font.'.
"""

# Because we want them:
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

from dataclasses import dataclass, field

from pygame import font

from pygame_gui.constants import Size


@dataclass
class Font:
    """The 'Font' class"""

    for_size: dict[Size, font.Font] = field(default_factory=dict)  # type: ignore


# Initialise the pygame font system.

font.init()

# FONT FUNCTIONS.
#   - create_font


def create_font(
    font_name: str, verysmall: int, small: int, normal: int, large: int, verylarge: int
) -> Font:
    """Creates a pygame_gui 'Font' object for each size."""

    _font: Font = Font()
    _font.for_size[Size.VERYSMALL] = font.SysFont(font_name, verysmall)
    _font.for_size[Size.SMALL] = font.SysFont(font_name, small)
    _font.for_size[Size.NORMAL] = font.SysFont(font_name, normal)
    _font.for_size[Size.LARGE] = font.SysFont(font_name, large)
    _font.for_size[Size.VERYLARGE] = font.SysFont(font_name, verylarge)

    return _font


# Create default fonts.

default_font: Font = create_font("arial", 10, 12, 14, 20, 26)
alternative_font: Font = create_font("timesnewroman", 12, 14, 18, 22, 28)


# Register font.

fonts: dict[str, Font] = {}
fonts["default"] = default_font
fonts["alternative"] = alternative_font
