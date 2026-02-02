"""
The 'button' module defines the 'Button' class.
"""

# Because pygame has no stub files.
# pylint: disable=no-member, no-name-in-module

# Because we want them:
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

from __future__ import annotations

from typing import Callable

from pygame import Surface, event

from pygame_gui.constants import Alignment, ControlType
from pygame_gui.frame import Frame
from pygame_gui.label import Label


class Button(Label):
    """The 'Button' class."""

    def __init__(
        self,
        parent: Frame | None,
        position: tuple[int, int],
        size: tuple[int, int],
        text: str,
        callback: Callable[[], None],
    ) -> None:

        # Initialise superclass.

        super().__init__(parent, position, size, text)

        # Set initial values.

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # Button style modifiers can be DEFAULT, OUTLINE or SIMPLE only.
        # Alignment is one of LEFT, RIGHT, CENTER.

        self._control_type: ControlType = ControlType.BUTTON
        self._alignment: Alignment = Alignment.CENTER
        self._callback: Callable[[], None] = callback

    # GAME LOOP FUNCTIONS.
    #   - handle_mouse_event
    #   - render

    def handle_mouse_event(self, event_to_handle: event.Event) -> bool:
        """Handles the mouse event."""

        # If the event is exhaustively handled then the method returns True.

        _event_handled: bool = super().handle_mouse_event(event_to_handle)

        # If the button has been pressed then invoke the callback.

        if not _event_handled and self.focussed and self.selected:
            self._callback()
            _event_handled = True

        return _event_handled

    def render(self, surface: Surface) -> None:
        """Renders the button."""

        # Allow superclass to draw the background, frame and text.

        super().render(surface)

        # Draw the selection indicator.

        if self.selected:
            self.draw_selection_indicator(surface, self.colors["selection"])
