"""
The 'menu' module defines the 'Menu' class.
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

from pygame import MOUSEBUTTONDOWN, event

from pygame_gui.constants import (
    DEFAULT_MENU_ITEM_HEIGHT,
    ControlType,
    Style,
    StyleModifier,
)
from pygame_gui.list_box import ListBox
from pygame_gui.panel import Panel


class Menu(Panel):
    """The 'Menu' class."""

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        texts: list[str],
        callback: Callable[[str], None],
        modal: bool = False,
        close_on_lost_focus: bool = True,
    ) -> None:
        """Initialises the Menu."""

        super().__init__(position, size, modal, close_on_lost_focus)

        # Save parameters.

        self._texts: list[str] = texts
        self._callback: Callable[[str], None] = callback

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # Frame style modifier can be DEFAULT only.

        self._control_type: ControlType = ControlType.MENU
        self._style: Style = Style.DEFAULT
        self._style_modifier: StyleModifier = StyleModifier.DEFAULT

        # Create the list box showing the menu items.

        self.create_list_box(self._texts)

    # PROPERTIES.
    #   - style

    @property
    def style(self) -> Style:
        """Returns '_style'."""

        # This is overridden from the Frame superclass
        # because we also need to update the list box.

        return self._style

    @style.setter
    def style(self, new_style: Style) -> None:
        """Sets '_style'."""

        # This is overridden from the Frame superclass
        # because we also need to update the list box.

        self._style = new_style
        self._list_box.style = new_style

    # GAME LOOP FUNCTIONS.
    #   - handle_mouse_event

    def handle_mouse_event(self, event_to_handle: event.Event) -> bool:
        """Handles the mouse event."""

        # If the event is exhaustively handled then the method returns True.

        _event_handled: bool = super().handle_mouse_event(event_to_handle)

        # If the event is a button press on the panel, then assume an item has been
        # selected from the list box and return True.

        if event_to_handle.type == MOUSEBUTTONDOWN:
            _event_handled = True

        # If the menu no longer has focus and the mouse button is pressed
        # then close the menu.

        if not self.focussed and event_to_handle.type == MOUSEBUTTONDOWN:

            self.showing = False

        return _event_handled

    # HELPER FUNCTIONS.
    #   - create_list_box
    #   - list_callback

    def create_list_box(self, texts: list[str]) -> None:
        """Creates the list box showing the menu items."""

        self._list_box: ListBox = ListBox(
            self, (0, 0), self.size, texts, DEFAULT_MENU_ITEM_HEIGHT, self.list_callback
        )
        self._list_box.style = Style.PRIMARY
        self._list_box.style_modifier = StyleModifier.DEFAULT

    def list_callback(self, selection: str) -> None:
        """The callback for the list box."""

        self.showing = False
        self._callback(selection)
