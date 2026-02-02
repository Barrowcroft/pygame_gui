"""
The 'list_box' module defines the 'ListBox' class.
"""

# Because pygame has no stub files.
# pylint: disable=no-member, no-name-in-module

# Because we want them:
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

from __future__ import annotations

from typing import Callable

from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, Rect, Surface, event

from pygame_gui.constants import ControlType, Style, StyleModifier
from pygame_gui.control import Control
from pygame_gui.draw import draw_rectangle
from pygame_gui.frame import Frame
from pygame_gui.list_box_item import ListBoxItem

SCROLLBAR_PADDING = 5


class ListBox(Frame):
    """The 'ListBox' class."""

    def __init__(
        self,
        parent: Control | None,
        position: tuple[int, int],
        size: tuple[int, int],
        items: list[str],
        item_height: int,
        callback: Callable[[str], None],
    ) -> None:

        # Initialise superclass.

        super().__init__(parent, position, size)

        # Set initial values.

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # Button style modifiers can be DEFAULT or OUTLINE  only.

        self._control_type: ControlType = ControlType.LISTBOX
        self._style: Style = Style.DEFAULT
        self._callback: Callable[[str], None] = callback

        # Initialise the list and list widgets.

        self._items: list[str] = items
        self._item_height: int = item_height
        self._item_top: int = 0

        self._item_widgets: list[ListBoxItem] = []

        # Initialise the scrollbar.

        self._scrollbar_max: int = 0
        self._scrollbar_min: int = 0
        self._scrollbar_moving: bool = False
        self._scrollbar_movement: int = 0
        self._scrollbar_size = self.get_scrollbar_size()
        self._scrollbar_position = self.get_scrollbar_position()

        # Create list item widgets.

        self.create_list_widgets()

    # PROPERTIES
    #   - style
    #   - style_modifier

    @property
    def style(self) -> Style:
        """Returns '_style'."""

        # This is overridden from the Frame superclass
        # because we also need to update the list widgets.

        return self._style

    @style.setter
    def style(self, new_style: Style) -> None:
        """Sets '_style'."""

        # This is overridden from the Frame superclass
        # because we also need to update the list widgets.

        self._style = new_style
        self.create_list_widgets()

    @property
    def style_modifier(self) -> StyleModifier:
        """Returns '_style_modifier'."""

        # This is overridden from the Frame superclass
        # because we also need to update the list widgets.

        return self._style_modifier

    @style_modifier.setter
    def style_modifier(self, new_style_modifier: StyleModifier) -> None:
        """Sets '_style_modifier'."""

        # This is overridden from the Frame superclass
        # because we also need to update the list widgets.

        self._style_modifier = new_style_modifier
        self.create_list_widgets()

    # GAME LOOP FUNCTIONS.
    #   - handle_mouse_event
    #   - update
    #   - render

    def handle_mouse_event(self, event_to_handle: event.Event) -> bool:
        """Handles the mouse event."""

        # If the event is exhaustively handled then the method returns True.

        _event_handled: bool = super().handle_mouse_event(event_to_handle)

        # If the control doesn't have focuss the cancel the moving state.

        if not self.focussed:
            self._scrollbar_moving = False

        # Ignore any events that are not button presses.

        if event_to_handle.type not in (
            MOUSEBUTTONDOWN,
            MOUSEMOTION,
        ):
            return _event_handled

        # Handle scrollbar movement.

        if not _event_handled and self.collides_with_scrollbar(event_to_handle):
            if event_to_handle.type == MOUSEBUTTONDOWN:
                self._scrollbar_moving = True

        if self.focussed and event_to_handle.type == MOUSEMOTION:
            self._scrollbar_movement = event_to_handle.pos[1]

        if event_to_handle.type == MOUSEBUTTONUP:
            self._scrollbar_moving = False

        return _event_handled

    def update(self, dt: float) -> None:
        """Updates the listbox.
        Ignores the delta time parameter."""

        # Calculate the position and size of the scrollbar.

        if self._scrollbar_moving:
            self._scrollbar_position = self.get_scrollbar_position()
            self._scrollbar_size = self.get_scrollbar_size()

        # Convert the scrollbar position to the item in the list
        # to set the top item according to the position of the scrollbar.

        if self._item_top != self.convert_scrollbar_position():

            self._item_top = self.convert_scrollbar_position()

            # Limit the top so that the bottom of the list is at the bottom
            # of the control.

            if len(self._items) > self.get_max_items_to_display():
                self._item_top = min(
                    self._item_top, len(self._items) - self.get_max_items_to_display()
                )
            else:
                self._item_top = 0

            self.create_list_widgets()

    def render(self, surface: Surface) -> None:
        """Renders the label."""

        # Allow superclass to draw the background and frame.

        super().render(surface)

        # Draw scrollbar, if needed.

        if len(self._items) > self.get_max_items_to_display():
            self.draw_scrollbar(surface)

    # HELPER FUNCTIONS.
    #   - create_list_widgets
    #   - get_scrollbar_position
    #   - get_scrollbar_sizeself.collides_with_scrollbar(event_to_handle)
    #   - get_minimum_postion_of_scrollbar
    #   - get_maximum_postion_of_scrollbar
    #   - get_max_items_to_display
    #   - draw_scrollbar
    #   - collides_with_scrollbar
    #   - convert_scrollbar_position

    def create_list_widgets(self) -> None:
        """Creates the list widgets."""

        _y_offset: int = 0

        self._children = []
        self._list_widgets = []

        for _index, _item in enumerate(
            self._items[self._item_top :], start=self._item_top
        ):

            if _y_offset + self._item_height >= self._size[1]:
                break

            _item_widget: ListBoxItem = ListBoxItem(
                self,
                (0, _y_offset),
                (self._size[0] - (SCROLLBAR_PADDING * 2), self._item_height),
                _item,
                self._callback,
            )
            _item_widget.style = self.style
            _item_widget.style_modifier = self.style_modifier
            self._item_widgets.append(_item_widget)

            _y_offset += self._item_height

    def get_scrollbar_position(self) -> tuple[int, int]:
        """Calculates the position of the scrollbar."""

        _x: int = (
            self.get_absolute_coordinates()[0] + self.size[0] - (SCROLLBAR_PADDING * 2)
        )

        _y: int = self._scrollbar_movement

        _y = max(self.get_minimum_postion_of_scrollbar(), _y)
        _y = min(self.get_maximum_postion_of_scrollbar(), _y)

        return (_x, _y)

    def get_scrollbar_size(self) -> tuple[int, int]:
        """Calculates the size of the scrollbar."""

        _num_items: int = len(self._items)
        _max_display: int = self.get_max_items_to_display()
        _width: int = 5
        _height: int = round(
            (self.size[1] - (SCROLLBAR_PADDING * 2)) * (_max_display / _num_items)
        )

        return (_width, _height)

    def get_minimum_postion_of_scrollbar(self) -> int:
        """Calculates the minimum y position of the scrollbar."""

        return self.get_absolute_coordinates()[1] + SCROLLBAR_PADDING

    def get_maximum_postion_of_scrollbar(self) -> int:
        """Calculates the maximum y position of the scrollbar."""

        return (
            self.get_absolute_coordinates()[1]
            + self.size[1]
            - SCROLLBAR_PADDING
            - self._scrollbar_size[1]
        )

    def get_max_items_to_display(self) -> int:
        """Calculates the maximum number of items that
        can be displayed for the given control size and item height."""

        return round((self.size[1] - (SCROLLBAR_PADDING * 2)) / self._item_height)

    def draw_scrollbar(self, surface: Surface) -> None:
        """Draws the scrollbar."""

        if self.colors["foreground"]:
            draw_rectangle(
                surface,
                self._scrollbar_position,
                self._scrollbar_size,
                self.colors["foreground"],
                self.border,
            )

    def collides_with_scrollbar(self, event_to_handle: event.Event) -> bool:
        """Check to see if mouse press event collides with the scrollbar."""

        _rect: Rect = Rect(
            self._scrollbar_position[0],
            self._scrollbar_position[1],
            self._scrollbar_size[0],
            self._scrollbar_size[1],
        )

        return _rect.collidepoint(event_to_handle.pos)

    def convert_scrollbar_position(self) -> int:
        """Converts the position of the scrollbar to a position
        in the list of items."""

        _size_of_scrollbar: int = self.size[1] - (SCROLLBAR_PADDING * 2)
        _number_of_items: int = len(self._items)

        _position_of_scrollbar: int = self._scrollbar_position[1] - (
            self.get_absolute_coordinates()[1] + SCROLLBAR_PADDING
        )

        return round(_position_of_scrollbar / (_size_of_scrollbar / _number_of_items))
