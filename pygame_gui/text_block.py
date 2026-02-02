"""
The 'text_block' module defines the 'TextBlock' class.
"""

# Because pygame has no stub files.
# pylint: disable=no-member, no-name-in-module

# Because we want them:
# pylint: disable=too-many-instance-attributes

from __future__ import annotations

from pygame import Surface

from pygame_gui.constants import Alignment, ControlType, Style, StyleModifier
from pygame_gui.control import Control
from pygame_gui.draw import draw_text
from pygame_gui.frame import Frame


class TextBlock(Frame):
    """The 'TextBlock' class."""

    def __init__(
        self,
        parent: Control | None,
        position: tuple[int, int],
        size: tuple[int, int],
        text: list[str],
    ) -> None:

        # Initialise superclass.

        super().__init__(parent, position, size)

        # Set initial values.

        self._text: list[str] = text

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # TextBlock style modifiers can be DEFAULT, OUTLINE or INVERSE only.
        # Alignment is one of LEFT, RIGHT, CENTER.

        self._control_type: ControlType = ControlType.TEXTBLOCK
        self._style: Style = Style.DEFAULT
        self._style_modifier: StyleModifier = StyleModifier.DEFAULT
        self._alignment: Alignment = Alignment.LEFT

    # PROPERTIES.
    #   - text
    #   - alignment

    @property
    def text(self) -> list[str]:
        """Returns '_text'."""
        return self._text

    @text.setter
    def text(self, new_text: list[str]) -> None:
        """Sets '_text'."""
        self._text = new_text

    @property
    def alignment(self) -> Alignment:
        """Returns '_alignment'."""
        return self._alignment

    @alignment.setter
    def alignment(self, new_alignment: Alignment) -> None:
        """Sets '_alignment'."""
        self._alignment = new_alignment

    # GAME LOOP FUNCTIONS.
    #   - render

    def render(self, surface: Surface) -> None:
        """Renders the text block."""

        # Allow superclass to draw the background and frame.

        super().render(surface)

        # Draw the caption.

        self.draw_text_block(surface, self.colors["foreground"])

    # HELPER FUNCTIONS.
    #   - draw_text_block

    def draw_text_block(self, surface: Surface, color: str | None) -> None:
        """Draws the text block."""

        if color and self.text:
            draw_text(
                surface,
                self.get_absolute_coordinates(),
                self.size,
                color,
                self.alignment,
                self.font,
                self.text,
            )
