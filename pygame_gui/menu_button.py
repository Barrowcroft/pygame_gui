"""
The 'menu_button' module defines the 'MenuButton' class.
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

from pygame_gui.constants import (
    DEFAULT_MENU_ITEM_HEIGHT,
    DEFAULT_MENUBUTTON_ITEMPADDING,
    DEFAULT_MENUBUTTON_TOPPADDING,
    Alignment,
    ControlType,
    Style,
)
from pygame_gui.frame import Frame
from pygame_gui.label import Label
from pygame_gui.menu import Menu


class MenuButton(Label):
    """The 'MenuButton' class."""

    def __init__(
        self,
        parent: Frame | None,
        position: tuple[int, int],
        size: tuple[int, int],
        callback: Callable[[str], None],
        texts: list[str],
    ) -> None:

        # Initialise superclass.

        super().__init__(parent, position, size, texts[0])

        # Save parameters.

        self._texts: list[str] = texts

        # Set initial values.

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # MenuButton style modifiers can be DEFAULT, OUTLINE or SIMPLE only.
        # Alignment is one of LEFT, RIGHT, CENTER.

        self._control_type: ControlType = ControlType.MENUBUTTON
        self._alignment: Alignment = Alignment.CENTER
        self._callback: Callable[[str], None] = callback

        # Create menu.

        self.create_menu(self._texts)

    # PROPERTIES.
    #   - style
    #   - menu

    @property
    def style(self) -> Style:
        """Returns '_style'."""

        # This is overridden from the Frame superclass
        # because we also need to update the menu.

        return self._style

    @style.setter
    def style(self, new_style: Style) -> None:
        """Sets '_style'."""

        # This is overridden from the Frame superclass
        # because we also need to update the menu.

        self._style = new_style
        self._menu.style = new_style

    @property
    def menu(self) -> Menu:
        """Returns '_menu'."""
        return self._menu

    @menu.setter
    def menu(self, new_menu: Menu) -> None:
        """Sets '_menu'."""
        self._menu = new_menu

    # GAME LOOP FUNCTIONS.
    #   - handle_mouse_event

    def handle_mouse_event(self, event_to_handle: event.Event) -> bool:
        """Handles the mouse event."""

        # If the event is exhaustively handled then the method returns True.

        _event_handled: bool = super().handle_mouse_event(event_to_handle)

        # If the menubutton is selected then show the menu.

        if self.selected:
            self._menu.showing = True

        return _event_handled

    # HELPER FUNCTIONS.
    #   - render_menu
    #   - get_menu_height
    #   - create_menu

    def render_menu(self, surface: Surface) -> None:
        """Renders the menu."""

        if self._menu.showing:
            self._menu.render(surface)

    def get_menu_height(self) -> int:
        """Calculates the required height of the menu."""

        _height: int = 0
        if len(self._texts) > 10:
            _height = DEFAULT_MENUBUTTON_TOPPADDING + (
                10 * DEFAULT_MENU_ITEM_HEIGHT + DEFAULT_MENUBUTTON_ITEMPADDING
            )
        else:
            _height = DEFAULT_MENUBUTTON_TOPPADDING + (
                len(self._texts)
                * (DEFAULT_MENU_ITEM_HEIGHT + DEFAULT_MENUBUTTON_ITEMPADDING)
            )

        return _height

    def create_menu(self, texts: list[str]) -> None:
        """Creates the menu."""

        self._menu: Menu = Menu(
            (
                self.get_absolute_coordinates()[0],
                self.get_absolute_coordinates()[1] + self.size[1] + 1,
            ),
            (self.size[0], self.get_menu_height() + 1),
            texts,
            self._callback,
            True,
            False,
        )
