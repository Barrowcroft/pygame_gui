"""
The 'entry_box' module defines the EntryBox control.
"""

# Because pygame has no stub files.
# pylint: disable=no-member, no-name-in-module
# pyright: reportUnknownMemberType=false
# pyright: reportAttributeAccessIssue=false

# Because we want them:
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

from typing import Callable, Tuple

from pygame import (
    K_BACKSPACE,
    K_DOWN,
    K_END,
    K_HOME,
    K_LEFT,
    K_LSHIFT,
    K_RETURN,
    K_RIGHT,
    K_RSHIFT,
    K_TAB,
    K_UP,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    Rect,
    Surface,
    draw,
    event,
    font,
)

from pygame_gui.constants import Alignment, ControlType, Style, StyleModifier
from pygame_gui.control import Control
from pygame_gui.font import Size, default_font
from pygame_gui.frame import Frame


class EntryBox(Frame):
    """The EntryBox control."""

    def __init__(
        self,
        parent: Control | None,
        position: Tuple[int, int],
        size: Tuple[int, int],
        text: str = "",
        callback_on_change: Callable[[str], None] | None = None,
        callback_on_exit: Callable[[str], None] | None = None,
        secret: bool = False,
    ) -> None:
        """Initialises the EntryBox control."""

        super().__init__(parent, position, size)

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # EntryBox style modifiers can be DEFAULT or OUTLINE only.
        # Alignment is one of LEFT, RIGHT, CENTER.

        self._control_type: ControlType = ControlType.ENTRYBOX
        self._style: Style = Style.DEFAULT
        self._style_modifier: StyleModifier = StyleModifier.DEFAULT
        self._alignment: Alignment = Alignment.LEFT

        # Save paramters.

        self._buffer: str = text
        self._secret: bool = secret

        # Save callbacks.

        self._callback_on_change: Callable[[str], None] | None = callback_on_change
        self._callback_on_lost_focus: Callable[[str], None] | None = callback_on_exit

        # Initialise other internals.

        self._cursor_pos: int = len(self._buffer)
        self._editing: bool = False

        # Special key handlers.

        self._key_actions: dict[int, Callable[[], None]] = {
            K_LEFT: self.move_left,
            K_RIGHT: self.move_right,
            K_HOME: self.move_home,
            K_END: self.move_end,
            K_BACKSPACE: self.handle_backspace,
        }

        self._ignored_keys = {
            K_RETURN,
            K_BACKSPACE,
            K_UP,
            K_DOWN,
            K_LEFT,
            K_RIGHT,
            K_HOME,
            K_END,
            K_LSHIFT,
            K_RSHIFT,
            K_TAB,
        }

    # PROPERTIES.
    #   - value
    #   - secret

    @property
    def value(self) -> str:
        """Sets the value of the entry box."""
        return self._buffer

    @value.setter
    def value(self, new_value: str) -> None:
        """gets the value of the entry box."""
        self._buffer = new_value
        self._cursor_pos: int = len(self._buffer)

    @property
    def secret(self) -> bool:
        """Sets the '_secret' value."""
        return self._secret

    @secret.setter
    def secret(self, new_secret: bool) -> None:
        """Return the '_secret' value."""
        self._secret = new_secret

    # GAME LOOP FUNCTIONS.
    #   - handle_key_event
    #   - handle_mouse_event
    #   - render

    def handle_key_event(self, event_to_handle: event.Event) -> bool:
        """Handles key events with cleaner, data-driven logic."""

        _event_handled: bool = super().handle_key_event(event_to_handle)

        # Ignore any events that are not key presses.

        if event_to_handle.type != KEYDOWN:
            return False

        # ControlState switching on RETURN.

        if event_to_handle.key in (K_RETURN, K_TAB):
            if self.focussed:
                if self._editing:
                    self.selected = False
                    self._editing = False
                    self.callback_on_lost_focus()
                else:
                    self.selected = True
                    self._editing = True
                    self._cursor_pos = len(self._buffer)
            else:
                if self._editing:
                    self.callback_on_lost_focus()
                self.focussed = False
                self.selected = False
                self._editing = False

        # Exit if not editing.

        if not self._editing:
            return False

        # Handle text input, some keys have special meaning and are ignored.

        if event_to_handle.key not in self._ignored_keys:
            self.handle_text_input(event_to_handle.unicode)

        # Handle the ignored keys.

        if (_handler := self._key_actions.get(event_to_handle.key)) is not None:
            _handler()

        return _event_handled

    def handle_mouse_event(self, event_to_handle: event.Event) -> bool:
        """Handles mouse events."""

        _event_handled: bool = super().handle_mouse_event(event_to_handle)

        # ControlState switching on MOUSEBUTTONDOWN.

        if event_to_handle.type == MOUSEBUTTONDOWN:
            if self.focussed:
                if self._editing:
                    self.selected = False
                    self._editing = False
                    self.callback_on_lost_focus()
                else:
                    self.selected = True
                    self._editing = True
                    self._cursor_pos = len(self._buffer)
            else:
                if self._editing:
                    self.callback_on_lost_focus()
                self.focussed = False
                self.selected = False
                self._editing = False

        if self._editing:
            self.selected = True

        return _event_handled

    def render(self, surface: Surface) -> None:
        """Renders the EntryBox control."""

        super().render(surface)

        if self.colors["foreground"]:

            # Render the text to a new surface.

            _text: str = self._buffer
            if self._secret:
                _text = "*" * len(self._buffer)

            _font: font.Font = default_font.for_size[Size.NORMAL]
            _text_surface = _font.render(_text, True, self.colors["foreground"])

            _rect = Rect(
                self.get_absolute_coordinates()[0],
                self.get_absolute_coordinates()[1],
                self._size[0],
                self._size[1],
            )

            # Align the text to the left (and vertically centered).

            _text_rect = _text_surface.get_rect()
            _text_rect.left = _rect.left + 5
            _text_rect.centery = _rect.centery

            _cursor_x: int = 20 + _font.size(_text[: self._cursor_pos])[0]

            if self.selected:
                draw.line(
                    surface,
                    self.colors["foreground"],
                    (
                        _cursor_x + self.get_absolute_coordinates()[0] - 15,
                        self.get_absolute_coordinates()[1] + 5,
                    ),
                    (
                        _cursor_x + self.get_absolute_coordinates()[0] - 15,
                        self.get_absolute_coordinates()[1] + _font.get_height() + 5,
                    ),
                )

            # Disaplay the text.

            surface.blit(_text_surface, _text_rect)

        # Draw the selection indicator.

        if self.focussed:
            self.draw_selection_indicator(surface, self.colors["selection"])

    # HELPER FUNCTIONS.
    #   - handle_text_input
    #   - handle_submit
    #   - handle_backspace
    #   - move_left
    #   - move_right
    #   - move_home
    #   - move_end
    #   - callback_on_lost_focus
    #   - calback_on_change

    def handle_text_input(self, char: str) -> None:
        """Insert a valid character into the buffer."""
        if len(self._buffer) >= 100:
            return
        if char.isalnum() or char in " -":
            self._buffer = (
                self._buffer[: self._cursor_pos]
                + char
                + self._buffer[self._cursor_pos :]
            )
            self._cursor_pos += 1
            self.calback_on_change()

    def handle_submit(self) -> None:
        """Commit input and exit editing mode."""
        self._buffer = self._buffer.strip()
        self.focussed = True
        self.selected = False

    def handle_backspace(self) -> None:
        """Handle backspace."""
        if self._cursor_pos > 0:
            self._buffer = (
                self._buffer[: self._cursor_pos - 1] + self._buffer[self._cursor_pos :]
            )
            self._cursor_pos -= 1
            self.calback_on_change()

    def move_left(self) -> None:
        """Move the cursor to the left."""
        if self._cursor_pos > 0:
            self._cursor_pos -= 1

    def move_right(self) -> None:
        """Move the cursor to the right."""
        if self._cursor_pos < len(self._buffer):
            self._cursor_pos += 1

    def move_home(self) -> None:
        """Move the cursor home."""
        self._cursor_pos = 0

    def move_end(self) -> None:
        """Move the cursor to the end of line."""
        self._cursor_pos = len(self._buffer)

    def callback_on_lost_focus(self) -> None:
        """Handles callback when entry looses focus"""

        self.value = self._buffer
        self._editing = False
        if self._callback_on_lost_focus:
            self._callback_on_lost_focus(self._buffer)

    def calback_on_change(self) -> None:
        """Handles callback when entry changes."""
        if self._callback_on_change:
            self._callback_on_change(self._buffer)
