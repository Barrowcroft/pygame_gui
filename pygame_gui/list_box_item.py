"""
The 'list_box_item' module defines the 'ListBoxItem' class.
"""

# Because pygame has no stub files.
# pylint: disable=no-member, no-name-in-module

# Because we want them:
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

from __future__ import annotations

from typing import Callable

from pygame import MOUSEBUTTONDOWN, Surface, event

from pygame_gui.constants import Alignment, ControlType, Style, StyleModifier
from pygame_gui.control import Control
from pygame_gui.draw import draw_string
from pygame_gui.frame import Frame


class ListBoxItem(Frame):
    """The 'ListBoxItem' class."""

    def __init__(
        self,
        parent: Control | None,
        position: tuple[int, int],
        size: tuple[int, int],
        text: str,
        callback: Callable[[str], None],
    ) -> None:

        # Initialise superclass.

        super().__init__(parent, position, size)

        # Set initial values.

        self._text: str = text
        self._callback: Callable[[str], None] = callback

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # ListBoxItem style modifiers can be DEFAULT or OUTLINE only.
        # Alignment is one of LEFT, RIGHT, CENTER.

        self._control_type: ControlType = ControlType.LISTBOXITEM
        self._style: Style = Style.DEFAULT
        self._style_modifier: StyleModifier = StyleModifier.DEFAULT
        self._alignment: Alignment = Alignment.LEFT

    # PROPERTIES.
    #   - text
    #   - alignment

    @property
    def text(self) -> str:
        """Returns '_text'."""
        return self._text

    @text.setter
    def text(self, new_text: str) -> None:
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
    #   - handle_mouse_event
    #   - render

    def handle_mouse_event(self, event_to_handle: event.Event) -> bool:
        """Handles the mouse event."""

        # If the event is exhaustively handled then the method returns True.

        _event_handled: bool = super().handle_mouse_event(event_to_handle)

        # Handle selection of the listbox item and invoke callback action.

        if event_to_handle.type == MOUSEBUTTONDOWN and self.selected:
            self._callback(self.text)

        return _event_handled

    def render(self, surface: Surface) -> None:
        """Renders the label."""

        # Allow superclass to draw the background and frame.

        super().render(surface)

        # Draw the text.

        self.draw_label(surface, self.colors["foreground"])

    # HELPER FUNCTIONS.
    #   - draw_label

    def draw_label(self, surface: Surface, color: str | None) -> None:
        """Draws the label."""

        if color and self.text:
            draw_string(
                surface,
                self.get_absolute_coordinates(),
                self.size,
                color,
                self.alignment,
                self.font,
                self.text,
            )
