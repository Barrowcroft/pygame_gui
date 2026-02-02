"""
The 'toggle_switch' module defines the 'ToggleSwitch' class.
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

from pygame_gui.constants import (
    DEFAULT_FRAME_BORDER_WIDTH,
    DEFAULT_FRAME_SELECTION_INDICATOR_INSET,
    DEFAULT_SWITCH_ROUNDEL_RADIUS,
    Alignment,
    ControlType,
)
from pygame_gui.draw import draw_circle
from pygame_gui.frame import Frame
from pygame_gui.label import Label
from pygame_gui.theme import colors_for


class ToggleSwitch(Label):
    """The 'ToggleSwitch' class."""

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

        # ToggleSwitches remain selected until explicitly cleared.

        self._sticky_select = True

        # Set initial values.

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # ToggleSwitch style modifier can be DEFAULT only.
        # Alignment is one of LEFT, RIGHT, CENTER.

        self._control_type: ControlType = ControlType.TOGGLESWITCH
        self._alignment: Alignment = Alignment.LEFT
        self._callback: Callable[[], None] = callback

    # GAME LOOP FUNCTIONS.
    #   - handle_mouse_event
    #   - render

    def handle_mouse_event(self, event_to_handle: event.Event) -> bool:
        """Handles the mouse event."""

        # If the event is exhaustively handled then the method returns True.

        _event_handled: bool = super().handle_mouse_event(event_to_handle)

        # If the button has been pressed then invoke the callback.

        if (
            not _event_handled
            and event_to_handle.type == MOUSEBUTTONDOWN
            and self.focussed
        ):
            self._callback()
            _event_handled = True

        return _event_handled

    def render(self, surface: Surface) -> None:
        """Renders the button."""

        # Allow superclass to draw the background, frame and text.

        super().render(surface)

        # Get the colors for the roundel.

        _roundel_colors = colors_for(
            ControlType.TOGGLESWITCHROUNDEL,
            self.style,
            self.style_modifier,
            self.focussed | self.selected,
        )

        # Draw the roundel.

        if self.selected:
            self.draw_roundel_background(surface, _roundel_colors["background"])

        self.draw_roundel_border(surface, _roundel_colors["border"])

        if self.focussed:
            self.draw_roundel_focus_indicator(surface, _roundel_colors["selection"])

    # HELPER FUNCTIONS.
    #   - get_roundel_position
    #   - draw_roundel_background
    #   - draw_roundel_border
    #   - draw_roundel_focus_indicator

    def get_roundel_position(self) -> tuple[int, int]:
        """Gets the position of the roundel."""

        # Calculate the roundel position.

        _x_position: int = (
            self.get_absolute_coordinates()[0]
            + self.size[0]
            - DEFAULT_SWITCH_ROUNDEL_RADIUS
        )

        _y_position: int = self.get_absolute_coordinates()[1] + round(self.size[1] / 2)

        # Return it!

        return _x_position, _y_position

    def draw_roundel_background(self, surface: Surface, color: str | None) -> None:
        """Draws the roundel's background rectangle."""

        # Draw the roundel.

        if color:
            draw_circle(
                surface,
                self.get_roundel_position(),
                DEFAULT_SWITCH_ROUNDEL_RADIUS,
                color,
            )

    def draw_roundel_border(self, surface: Surface, color: str | None) -> None:
        """Draws the roundel's border rectangle."""

        if color:
            draw_circle(
                surface,
                self.get_roundel_position(),
                DEFAULT_SWITCH_ROUNDEL_RADIUS,
                color,
                DEFAULT_FRAME_BORDER_WIDTH,
            )

    def draw_roundel_focus_indicator(self, surface: Surface, color: str | None) -> None:
        """Draws the roundel's focus rectangle."""

        if color:
            draw_circle(
                surface,
                self.get_roundel_position(),
                DEFAULT_SWITCH_ROUNDEL_RADIUS,
                color,
                DEFAULT_FRAME_BORDER_WIDTH,
                DEFAULT_FRAME_SELECTION_INDICATOR_INSET,
            )
