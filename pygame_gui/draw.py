"""
The 'draw' module defines the drawing functions.
"""

# Because we want them:
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

from pygame import Color, Rect, Surface, draw, font, gfxdraw

from pygame_gui.constants import (
    DEFAULT_TEXT_HORIZONTAL_PADDING,
    DEFAULT_TEXT_VERTICAL_PADDING,
    Alignment,
)

# Functions in this module.
#   - draw_rectangle
#   - draw_string
#   - draw_text
#   - draw_circle


def draw_rectangle(
    surface: Surface,
    position: tuple[int, int],
    size: tuple[int, int],
    color: str,
    boarder: tuple[int, int, int, int],
    boarder_width: int = 0,
    inset: int = 0,
) -> None:
    """Draws a rectangle with the given colour."""

    # If the border width is zero then a filled rectangle
    # will be drawn. The border radius is the radius of the
    # corners of the rectangle.

    draw.rect(
        surface,
        color,
        (
            position[0] + inset,
            position[1] + inset,
            size[0] - (inset * 2),
            size[1] - (inset * 2),
        ),
        boarder_width,
        border_top_left_radius=boarder[0],
        border_top_right_radius=boarder[1],
        border_bottom_left_radius=boarder[2],
        border_bottom_right_radius=boarder[3],
    )


def draw_string(
    surface: Surface,
    position: tuple[int, int],
    size: tuple[int, int],
    color: str,
    alignment: Alignment,
    text_font: font.Font,
    text: str,
) -> None:
    """Draws text to the surface."""

    # Create the text surface.

    _text_surface: Surface = text_font.render(
        text,
        True,
        color,
    )
    _rect = Rect(
        position[0],
        position[1],
        size[0],
        size[1],
    )

    # Center the text in the rectangle, by default.

    _text_rect = _text_surface.get_rect(center=_rect.center)

    # Re-align if required.

    if alignment == Alignment.LEFT:
        _text_rect = _text_surface.get_rect(
            midleft=(_rect.left + 5, _rect.centery)  # 5px padding
        )

    if alignment == Alignment.RIGHT:
        _text_rect = _text_surface.get_rect(
            midright=(_rect.right - 5, _rect.centery)  # 5px padding from the right
        )

    # Display the text.

    old_clip = surface.get_clip()  # Save current clip
    surface.set_clip(_rect)  # Limit drawing to _rect

    surface.blit(_text_surface, _text_rect)

    surface.set_clip(old_clip)  # Restore previous clip


def draw_text(
    surface: Surface,
    position: tuple[int, int],
    size: tuple[int, int],
    color: str,
    alignment: Alignment,
    text_font: font.Font,
    text: list[str],
) -> None:
    """Draws text to the surface."""

    # Draw the text to the surface.

    _y_pos: int = position[1] + DEFAULT_TEXT_VERTICAL_PADDING

    for _text in text:

        _text_surface: Surface = text_font.render(
            _text,
            True,
            color,
        )

        # Calculate the text target rectangle.

        _, height = _text_surface.get_size()

        _rect = Rect(
            position[0] + DEFAULT_TEXT_HORIZONTAL_PADDING,
            _y_pos,
            size[0] - (DEFAULT_TEXT_HORIZONTAL_PADDING * 2),
            height,
        )

        # Center the text in the rectangle, by default.

        _text_rect = _text_surface.get_rect(center=_rect.center)

        # Re-align if required.

        if alignment == Alignment.LEFT:
            _text_rect = _text_surface.get_rect(
                midleft=(_rect.left + 5, _rect.centery)  # 5px padding
            )

        if alignment == Alignment.RIGHT:
            _text_rect = _text_surface.get_rect(
                midright=(_rect.right - 5, _rect.centery)  # 5px padding from the right
            )

        # Display the text.

        old_clip = surface.get_clip()  # Save current clip
        surface.set_clip(_rect)  # Limit drawing to _rect

        surface.blit(_text_surface, _text_rect)

        surface.set_clip(old_clip)  # Restore previous clip

        # Update _y_pos.

        _y_pos += height


def draw_circle(
    surface: Surface,
    position: tuple[int, int],
    size: int,
    color: str,
    boarder_width: int = 0,
    inset: int = 0,
) -> None:
    """Draws a circle with the given colour."""

    # The radius i half the size.

    _radius: int = int(size / 2)

    # If the boarder width is zero then draw a filled circle.

    if boarder_width == 0:
        gfxdraw.filled_circle(  # pylint: disable=I1101
            surface, position[0], position[1], _radius - inset, Color(color)
        )

    # Otherwise draw a normal circle.

    else:
        gfxdraw.aacircle(  # pylint: disable=I1101
            surface,
            position[0],
            position[1],
            _radius - inset,
            Color(color),
        )
