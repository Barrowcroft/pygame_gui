"""
The 'slider' module defines the Slider class.
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

from typing import Callable

from pygame import MOUSEMOTION, Surface, event

from pygame_gui.constants import ControlType, Style, StyleModifier
from pygame_gui.control import Control
from pygame_gui.draw import draw_rectangle
from pygame_gui.frame import Frame
from pygame_gui.roundel import Roundel


class Slider(Frame):
    """The Slider class."""

    def __init__(
        self,
        parent: Control | None,
        position: tuple[int, int],
        size: tuple[int, int],
        callback: Callable[[int], None],
        percent: int = 0,
    ) -> None:
        """Initialises the Slider."""

        # Initialise the superclass.

        super().__init__(parent, position, size)

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # Slider style modifiers can be DEFAULT, OUTLINE or INVERSE only.

        self._control_type: ControlType = ControlType.SLIDER
        self._style: Style = Style.DEFAULT
        self._style_modifier: StyleModifier = StyleModifier.DEFAULT

        # Save parameters.

        self._callback: Callable[[int], None] = callback
        self._percent: int = percent

        # Create roundel.

        self.create_roundel()

    # PROPERTIES
    #   - style
    #   - style_modifier
    #   - percent

    @property
    def style(self) -> Style:
        """Returns '_style'."""

        # This is overridden from the Frame superclass
        # because we also need to update the roundel.

        return self._style

    @style.setter
    def style(self, new_style: Style) -> None:
        """Sets '_style'."""

        # This is overridden from the Frame superclass
        # because we also need to update the roundel.

        self._style = new_style
        self._roundel.style = new_style

    @property
    def style_modifier(self) -> StyleModifier:
        """Returns '_style_modifier'."""

        # This is overridden from the Frame superclass
        # because we also need to update the roundel.

        return self._style_modifier

    @style_modifier.setter
    def style_modifier(self, new_style_modifier: StyleModifier) -> None:
        """Sets '_style_modifier'."""

        # This is overridden from the Frame superclass
        # because we also need to update the roundel.

        self._style_modifier = new_style_modifier
        self._roundel.style_modifier = new_style_modifier

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
    #   - handle_mouse_event
    #   - render

    def handle_mouse_event(self, event_to_handle: event.Event) -> bool:
        """Handles mouse events. Returning True indicates that
        the event has been exhaustively dealt with."""

        _event_handled: bool = super().handle_mouse_event(event_to_handle)

        # If the control does not have focus then there is nothing to do.

        if not self.focussed:
            return _event_handled

        # If the event id not MOUSEMOTION then there is nothing to do.

        if event_to_handle.type != MOUSEMOTION:
            return _event_handled

        # If the event is MOUSEMOTION adjust the position of the roundel.

        if event_to_handle.buttons[0]:

            _position: int = event_to_handle.pos[0] - self.get_absolute_coordinates()[0]
            _position = max(_position, round(self.get_roundel_size() / 2))
            _position = min(
                _position, self.size[0] - round(self.get_roundel_size() / 2)
            )

            self._roundel.position = (
                _position,
                self._roundel.position[1],
            )

            self._callback(self.convert_x_pos_to_percent())

        return _event_handled

    def render(self, surface: Surface) -> None:
        """Renders the Slider control."""

        # Allow superclass to render background and frame.

        super().render(surface)

        # Get appropriate color for the slider line.

        _line_color: str | None = self.colors["foreground"]

        # Draw the line.

        if _line_color:
            draw_rectangle(
                surface,
                self.get_line_position(),
                self.get_line_size(),
                _line_color,
                self.border,
            )

        # Redraw the roundel over the line

        self._roundel.render(surface)

    # HELPER FUNCTIONS.
    #   - get_line_position
    #   - get_line_size
    #   - get_line_length
    #   - get_roundel_position
    #   - get_roundel_size
    #   - create_roundel
    #   - get_minimum_x_position_for_roundel
    #   - get_maximum_x_position_for_roundel
    #   - convert_percent_to_x_pos
    #   - convert_x_pos_to_percent

    def get_line_position(self) -> tuple[int, int]:
        """Calculates the position of the slider line."""

        return (
            self.get_absolute_coordinates()[0],
            self.get_absolute_coordinates()[1] + round(self.size[1] / 2),
        )

    def get_line_size(self) -> tuple[int, int]:
        """Calculates the size of the slider line."""

        return (self.size[0], 1)

    def get_line_length(self) -> int:
        """Calculates the length of the slider line."""

        return (
            self.get_maximum_x_position_for_roundel()
            - self.get_minimum_x_position_for_roundel()
        )

    def get_roundel_position(self) -> tuple[int, int]:
        """Calculates the roundel's position."""

        return (
            self.convert_percent_to_x_pos(),
            round(self.size[1] / 2),
        )

    def get_roundel_size(self) -> int:
        """Calculates the roundel's size."""

        return round(self.size[1] / 2)

    def create_roundel(self) -> None:
        """Creates the roundel."""

        self._roundel: Roundel = Roundel(
            self,
            self.get_roundel_position(),
            (self.get_roundel_size(), self.get_roundel_size()),
        )
        self._roundel.style = Style.DEFAULT
        self._roundel.style_modifier = self.style_modifier

    def get_minimum_x_position_for_roundel(self) -> int:
        """Calculates the minimum x position for the rounbdel ."""

        return self.get_absolute_coordinates()[0] - round(self.get_roundel_size() / 2)

    def get_maximum_x_position_for_roundel(self) -> int:
        """Calculates the maximum x position for the rounbdel ."""

        return (
            self.get_absolute_coordinates()[0]
            + self.size[0]
            - round(self.get_roundel_size() / 2)
        )

    def convert_percent_to_x_pos(self) -> int:
        """Converts the percent to the x position of the roundel."""

        _1_percent: float = self.get_line_length() / 100

        return round(_1_percent * self.percent)

    def convert_x_pos_to_percent(self) -> int:
        """Converts the x position of the roundel
        to a percentage of the size of the scale."""

        # Center of roundel
        x: int = self._roundel.position[0]

        # Roundel radius
        r: int = round(self.get_roundel_size() / 2)

        # Center min/max (in slider local space)
        center_min: int = r
        center_max: int = self.size[0] - r

        # Convert center_x from absolute → local
        x_local: int = x

        # Percent
        percent = 100 * (x_local - center_min) / (center_max - center_min)
        return round(max(0, min(100, percent)))
