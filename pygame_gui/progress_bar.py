"""
The 'progress_bar' module defines the ProgressBar class.
"""

# Because pygame has no stub files.
# pylint: disable=no-member, no-name-in-module
# pyright: reportUnknownMemberType=false
# pyright: reportAttributeAccessIssue=false

# Because we want them:
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

from __future__ import annotations

from pygame import Surface

from pygame_gui.constants import Alignment, ControlType, Style, StyleModifier
from pygame_gui.control import Control
from pygame_gui.draw import draw_rectangle, draw_string
from pygame_gui.frame import Frame


class ProgressBar(Frame):
    """The ProgressBar class."""

    def __init__(
        self,
        parent: Control | None = None,
        position: tuple[int, int] = (0, 0),
        size: tuple[int, int] = (100, 30),
        text: str = "",
        percent: int = 0,
    ) -> None:
        """Initialises the ProgressBar."""

        # Initialise the superclass.

        super().__init__(parent, position, size)

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # ProgressBar style modifiers can be DEFAULT or INVERSE only.
        # Alignment is one of LEFT, RIGHT, CENTER.

        self._control_type: ControlType = ControlType.PROGRESSBAR
        self._style: Style = Style.DEFAULT
        self._style_modifier: StyleModifier = StyleModifier.DEFAULT
        self._alignment: Alignment = Alignment.CENTER

        # Save parameters and initialise.

        self._text: str = text
        self._progress_text: str = f"{text} {str(percent)}%"
        self._percent: int = percent

    # PROPERTIES
    #   - percent

    @property
    def percent(self) -> int:
        """Returns the current '_percent' value=."""
        return self._percent

    @percent.setter
    def percent(self, new_percent: int) -> None:
        """Sets the '_percent' value=."""
        self._progress_text: str = f"{self._text} {str(new_percent)}%"
        self._percent = new_percent

    # GAME LOOP FUNCTIONS
    #   - render

    def render(self, surface: Surface) -> None:
        """Renders the ProgressBar control."""

        # Allow superclass to render background and frame.

        super().render(surface)

        # Get the appropriate colors.

        _indicator_color: str | None = self.colors["selection"]
        _text_color: str | None = self.colors["foreground"]

        # Draw the progress indicator.

        if _indicator_color:
            draw_rectangle(
                surface,
                self.get_position_of_indicator(),
                self.get_size_of_indicator(),
                _indicator_color,
                self.border,
            )

        # Draw the text.

        if _text_color:
            draw_string(
                surface,
                self.get_absolute_coordinates(),
                self._size,
                _text_color,
                self._alignment,
                self.font,
                self._progress_text,
            )

    # HELPER FUNCTIONS.
    #   - get_position_of_indicator
    #   - get_size_of_indicator

    def get_position_of_indicator(self) -> tuple[int, int]:
        """Gets the position of the indicator."""

        return (
            self.get_absolute_coordinates()[0],
            self.get_absolute_coordinates()[1],
        )

    def get_size_of_indicator(self) -> tuple[int, int]:
        """Gets the size of the indicator based on percentage progress."""

        _bar_size: int = self._size[0]
        _progress: int = round((_bar_size / 100) * self._percent)

        return (_progress, self._size[1])
