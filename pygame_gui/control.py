"""
The 'control' module defines the 'Control' class.
The control is the base class upon which all other pygame_gui components are based,
and it holds the properties and methods that are common to all pygame_gui components.
"""

# Because pygame has no stub files.
# pylint: disable=no-member, no-name-in-module

# Because we want them:
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument

from __future__ import annotations

from pygame import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    MOUSEWHEEL,
    Rect,
    Surface,
    display,
    event,
)


class Control:
    """The 'Control' class."""

    def __init__(
        self, parent: Control | None, position: tuple[int, int], size: tuple[int, int]
    ) -> None:

        # Save a link to the parent and if the parent is not None
        # register this control as a child of it's parent.

        self._parent: Control | None = parent
        if self._parent is not None:
            self._parent.add_child(self)

        # Set initial metric values.

        self._position: tuple[int, int] = position
        self._size: tuple[int, int] = size

        # Set initial state values.
        # If the control has 'sticky_select' set to True,
        # then it will not automatically become unselected when
        # the control looses focus.

        self._disabled: bool = False
        self._focussed: bool = False
        self._selected: bool = False
        self._sticky_select: bool = False

        # Check size of control againt parent.

        self.check_fits_inside_available_space()

        # Initialise the list of child controls.

        self._children: list[Control] = []

    # PROPERTIES.
    #   - position
    #   - size
    #   - disabled
    #   - focussed
    #   - selected
    #   - sticky_select

    @property
    def position(self) -> tuple[int, int]:
        """Returns '_position'."""
        return self._position

    @position.setter
    def position(self, new_position: tuple[int, int]) -> None:
        """Sets '_position'."""

        self._position = new_position

    @property
    def size(self) -> tuple[int, int]:
        """Returns '_size'."""
        return self._size

    @size.setter
    def size(self, new_size: tuple[int, int]) -> None:
        """Sets '_size'."""
        self._size = new_size

    @property
    def disabled(self) -> bool:
        """Returns '_disabled'."""
        return self._disabled

    @disabled.setter
    def disabled(self, new_disabled: bool) -> None:
        """Sets '_disabled'."""
        self._disabled = new_disabled

    @property
    def focussed(self) -> bool:
        """Returns '_focussed'."""
        return self._focussed

    @focussed.setter
    def focussed(self, new_focussed: bool) -> None:
        """Sets '_focussed'."""
        self._focussed = new_focussed

    @property
    def selected(self) -> bool:
        """Returns '_selected'."""
        return self._selected

    @selected.setter
    def selected(self, new_selected: bool) -> None:
        """Sets '_selected'."""
        self._selected = new_selected

    @property
    def sticky_select(self) -> bool:
        """Returns '_sticky_select'."""
        return self._sticky_select

    @sticky_select.setter
    def sticky_select(self, new_sticky_select: bool) -> None:
        """Sets '_sticky_select'."""
        self._sticky_select = new_sticky_select

    # GAME LOOP FUNCTIONS.
    #   - handle_key_event
    #   - handle_mouse_event
    #   - handle_joystick_event
    #   - update
    #   - render

    def handle_key_event(self, event_to_handle: event.Event) -> bool:
        """Handles the key press event."""

        # If the event is exhaustively handled then the method returns True.

        _event_handled: bool = False

        # If the control is disabled there is nothing to do.

        if self.disabled:
            return False

        # Give an opportuniy to each of the child controls
        # to handle the event.

        for _child in self.get_children():
            if _child.handle_key_event(event_to_handle):
                _event_handled = True
                break

        return _event_handled

    def handle_mouse_event(self, event_to_handle: event.Event) -> bool:
        """Handles the mouse event."""

        # If the event is exhaustively handled then the method returns True.

        _event_handled: bool = False

        # If the control is disabled there is nothing to do.

        if self.disabled:
            self.focussed = False
            self.selected = False
            return _event_handled

        # If the event is a mouse wheel movement ignore it.

        if self.unwanted_mouse_input(event_to_handle):
            return _event_handled

        # If the event is not a mouse move or mouse click event
        # then there is nothing to do.

        if event_to_handle.type not in (MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP):
            return False

        # If the event has not been handled then check to see if it
        # collides with the control.

        _collides: bool = self.collides_with_control(event_to_handle)

        # If it does, and the event was a
        # mouse motion, then the control becomes focussed.
        # If it does, and the event was a mouse click, then the control
        # becomes focussed and selected.

        if _collides and event_to_handle.type == MOUSEMOTION:
            self.focussed = True
            if not self.sticky_select:
                self.selected = False

        if _collides and event_to_handle.type == MOUSEBUTTONDOWN:
            self.focussed = True
            if self.selected and self.sticky_select:
                self.selected = False
            else:
                self.selected = True

        # If the event does not collide with the control then the
        # control looses its focus. If the control is not set to
        # 'sticky_select' then it will also become unselected.

        if not _collides:
            self.focussed = False

        if not _collides and not self.sticky_select:
            self.selected = False

        # Now give an opportuniy to each of the child controls
        # to handle the event.

        for _child in self.get_children():
            if _child.handle_mouse_event(event_to_handle):
                _event_handled = True
                break

        return _event_handled

    def handle_joystick_event(self, event_to_handle: event.Event) -> bool:
        """Handles the key press event."""
        # Not handling this for now!""
        return False

    def update(self, dt: float) -> None:
        """Updates the control."""

        # Now give an opportuniy to each of the child controls
        # to update.

        for _child in self.get_children():
            if _child.update(dt):
                break

    def render(self, surface: Surface) -> None:
        """Renders the control."""
        # Not handling this for now!
        # Will be handled by subclasses when appropriate.""

    # HELPER FUNCTIONS.
    #   - get_absolute_coordinates
    #   - collides_with_control
    #   - check_fits_inside_available_space
    #   - add_child
    #   - get_children
    #   - unwanted_mouse_input

    def get_absolute_coordinates(self) -> tuple[int, int]:
        """Returns the absolute coordinates of the control."""

        # If the control has no parents then its position coordinates are absolute.
        # If the control has a parent then add the controls position coordinates to
        # the parents absolute coordinates.

        if self._parent is None:
            return self.position

        return (
            self._parent.get_absolute_coordinates()[0] + self.position[0],
            self._parent.get_absolute_coordinates()[1] + self.position[1],
        )

    def collides_with_control(self, event_to_handle: event.Event) -> bool:
        """Check to see if mouse press event collides with the control."""

        # This is overridden in the case of the Roundel because
        # its collision is within a circle not a rectanlge.

        _rect = Rect(
            self.get_absolute_coordinates()[0],
            self.get_absolute_coordinates()[1],
            self.size[0],
            self.size[1],
        )
        return _rect.collidepoint(event_to_handle.pos)

    def check_fits_inside_available_space(self) -> None:
        """Check that this control fits inside the space allocated
        to the parent control, if there is one, otherwise check it fits
        in the application window."""

        # Check Control fits in parent.

        if self._parent:
            if (
                self.position[0] + self.size[0] > self._parent.size[0]
                or self.position[1] + self.size[1] > self._parent.size[1]
            ):
                raise ValueError(
                    f"Control size {self.size} at {self.position} "
                    + f"does not fit in parent Control {self._parent.size}."
                )
            return

        # No parent, so check Control fits in application window.

        _window: Surface = display.get_surface()
        if _window:
            if (
                self.position[0] + self.size[0] > _window.get_size()[0]
                or self.position[1] + self.size[1] > _window.get_size()[1]
            ):
                raise ValueError(
                    f"Control size {self.size} at {self.position} does not fit in pygame window."
                )
            return

        # If there is no parent and no window,
        # we have a terminal error condition.

        raise ValueError("Expected a valid Pygame window (Surface), but got None.")

    def add_child(self, child: Control) -> None:
        """Adds a child control to this control's list of children."""

        self._children.append(child)

    def get_children(self) -> list[Control]:
        """Returns the control's children."""

        return self._children

    def unwanted_mouse_input(self, event_to_handle: event.Event) -> bool:
        """Check to see if the event is generated by the mouse wheel.
        This is to exclude 'noise' from the mouse wheel."""

        if event_to_handle.type == MOUSEWHEEL:
            return True

        if event_to_handle.type in (
            MOUSEBUTTONDOWN,
            MOUSEBUTTONUP,
        ) and event_to_handle.button in (
            4,
            5,
            6,
            7,
        ):
            return True

        return False
