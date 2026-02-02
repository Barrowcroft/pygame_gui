"""
The 'roundel' module defines the Roundel class.
This is a subclass of Frame, with the drawing and collision
detection functions overridden to allow for it's circular form.
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

from pygame import Surface, event, mouse

from pygame_gui.constants import (
    DEFAULT_FRAME_BORDER_WIDTH,
    DEFAULT_FRAME_SELECTION_INDICATOR_INSET,
    ControlType,
    Style,
    StyleModifier,
)
from pygame_gui.control import Control
from pygame_gui.draw import draw_circle
from pygame_gui.frame import Frame


class Roundel(Frame):
    """The Roundel class."""

    def __init__(
        self,
        parent: Control | None = None,
        position: tuple[int, int] = (0, 0),
        size: tuple[int, int] = (30, 30),
    ) -> None:
        """Initialises the frame."""

        # Initialise the superclass.

        super().__init__(parent, position, size)

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # Roundel style modifiers can be DEFAULT, OUTLINE or INVERSE only.

        self._control_type: ControlType = ControlType.ROUNDEL
        self._style: Style = Style.DEFAULT
        self._style_modifier: StyleModifier = StyleModifier.DEFAULT

        # Check size meets requirements.

        self.check_size()

    # GAME LOOP FUNCTIONS.
    #   - render

    def render(self, surface: Surface) -> None:
        """Renders the button."""

        # Allow superclass to draw the background, frame and text.

        super().render(surface)

        # Draw the selection indicator.

        if self.focussed:
            self.draw_selection_indicator(surface, self.colors["selection"])

    # HELPER FUNCTIONS.
    #   - check_fits_inside_available_space
    #   - check_size
    #   - collides_with_control
    #   - get_roundel_position
    #   - draw_background
    #   - draw_boarder
    #   - draw_selection_indicator

    def check_fits_inside_available_space(self) -> None:
        """This overrides the function in the Control superclass.
        Users of the Roundel are responsible for making sure it fits."""

        # This essentially cancels the check.

    def check_size(self) -> None:
        """Checks the size to ensure that the width and height
        are the same. If not then the height will be set the same as the width."""

        if self._size[1] != self._size[0]:
            self._size = (self._size[0], self._size[0])

    def collides_with_control(self, event_to_handle: event.Event) -> bool:
        """Checks to see if the positon of the click is inside a circle
        at a given position with a given radius."""

        _circle_centre: tuple[int, int] = (
            self.get_absolute_coordinates()[0],
            self.get_absolute_coordinates()[1],
        )
        _radius: int = int(self._size[0] / 2)
        _click_position: tuple[int, int] = mouse.get_pos()

        dx = _click_position[0] - _circle_centre[0]
        dy = _click_position[1] - _circle_centre[1]
        distance_squared = dx * dx + dy * dy

        if distance_squared <= (_radius * _radius):
            return True

        return False

    def get_roundel_position(self) -> tuple[int, int]:
        """Gets the position of the roundel."""

        return (
            self.get_absolute_coordinates()[0],
            self.get_absolute_coordinates()[1],
        )

    def draw_background(self, surface: Surface, color: str | None) -> None:
        """Draws the roundel's background cicle."""

        # This overrides the method in the Frame superclass
        # because we are drawing a circle not a rectangle.

        if color:

            draw_circle(
                surface,
                self.get_roundel_position(),
                self._size[0],
                color,
            )

    def draw_boarder(self, surface: Surface, color: str | None) -> None:
        """Draws the roundel's foreground circle."""

        # This overrides the method in the Frame superclass
        # because we are drawing a circle not a rectangle.

        if color:
            draw_circle(
                surface,
                self.get_roundel_position(),
                self._size[0],
                color,
                DEFAULT_FRAME_BORDER_WIDTH,
            )

    def draw_selection_indicator(self, surface: Surface, color: str | None) -> None:
        """Draws the roundel's focus circle."""

        # This overrides the method in the Frame superclass
        # because we are drawing a circle not a rectangle.

        if color:
            draw_circle(
                surface,
                self.get_roundel_position(),
                self._size[0],
                color,
                DEFAULT_FRAME_BORDER_WIDTH,
                DEFAULT_FRAME_SELECTION_INDICATOR_INSET,
            )
