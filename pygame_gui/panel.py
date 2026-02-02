"""
The 'panel' module defines the 'Panel' class.
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

from pygame import Surface, event

from pygame_gui.constants import (
    DEFAULT_PANEL_SHADOW_COLOR,
    ControlType,
    Style,
    StyleModifier,
)
from pygame_gui.draw import draw_rectangle
from pygame_gui.frame import Frame


class Panel(Frame):
    """The 'Panel' class."""

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        modal: bool = False,
        close_on_lost_focus: bool = True,
    ) -> None:
        """Initialises the Panel."""

        super().__init__(None, position, size)

        # Save parameters.

        # If the panel is modal it will consume all events.

        self._modal: bool = modal

        self._close_on_lost_focus: bool = close_on_lost_focus

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # Frame style modifier can be DEFAULT only.

        self._control_type: ControlType = ControlType.PANEL
        self._style: Style = Style.DEFAULT
        self._style_modifier: StyleModifier = StyleModifier.DEFAULT

        # Initialise other internals.

        self._showing: bool = False

    # PROPERTIES.
    #   - showing
    #   - close_on_lost_focus

    @property
    def showing(self) -> bool:
        """Returns the current '_showing' value."""
        return self._showing

    @showing.setter
    def showing(self, new_showing: bool) -> None:
        """Sets the '_showing' value."""
        self._showing = new_showing

    @property
    def close_on_lost_focus(self) -> bool:
        """Returns the current '_close_on_lost_focus' value."""
        return self._close_on_lost_focus

    @close_on_lost_focus.setter
    def close_on_lost_focus(self, new_close_on_lost_focus: bool) -> None:
        """Sets the '_close_on_lost_focus' value=."""
        self._close_on_lost_focus = new_close_on_lost_focus

    # GAME LOOP FUNCTIONS
    #   - handle_mouse_event
    #   - render

    def handle_mouse_event(self, event_to_handle: event.Event) -> bool:
        """Handles mouse events.
        Returning True indicates that the event has been exhaustively dealt
        with and that no futher Frames should be given the opportunity
        to repsond to the event."""

        _event_handled: bool = super().handle_mouse_event(event_to_handle)

        # Dont handle events if not showing.

        if not _event_handled and self._showing:

            # If the panel has focus it will consume all events.

            if self.focussed:
                _event_handled = True

            # If the panel is modal it will consume all events,
            # even if it doesn't have focus.

            if self._modal:
                _event_handled = True

            # If the panel is supposed to close on lost focus then close it.

            if not self.focussed and self._close_on_lost_focus:
                self._showing = False

        return _event_handled

    def render(self, surface: Surface) -> None:
        """Renders the frame."""

        # If we are showing then let the superclass render the frame.

        if self._showing:
            self.draw_shadow(surface)
            super().render(surface)

    # HELPER FUNCTIONS.
    #   - check_fits_inside_available_space
    #   - draw_shadow

    def check_fits_inside_available_space(self) -> None:
        """Check that this control fits inside the space allocated
        to the parent control"""

        # This function overrides that in the Control superclass
        # because panels do not have to fit within their parent
        # control.

        # Nothing to do... Saul Goodman

    def draw_shadow(self, surface: Surface) -> None:
        """Draws the panel's shadow rectangle."""

        _background: str = DEFAULT_PANEL_SHADOW_COLOR
        draw_rectangle(
            surface,
            (
                self.get_absolute_coordinates()[0] + 3,
                self.get_absolute_coordinates()[1] + 3,
            ),
            self._size,
            _background,
            self.border,
        )
