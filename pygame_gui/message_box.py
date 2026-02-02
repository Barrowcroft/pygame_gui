"""
The 'message_box' module defines the 'MessageBox' class.
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

from functools import partial
from typing import Callable

from pygame import Surface, display

from pygame_gui.button import Button
from pygame_gui.constants import (
    DEFAULT_MESSAGEBOX_BARHEIGHT,
    DEFAULT_MESSAGEBOX_BUTTONHEIGHT,
    DEFAULT_MESSAGEBOX_BUTTONSPACING,
    DEFAULT_MESSAGEBOX_BUTTONWIDTH,
    DEFAULT_MESSAGEBOX_SPACEFROMBOTTOM,
    DEFAULT_MESSAGEBOX_VERTICALPADDING,
    Alignment,
    ControlType,
    Style,
    StyleModifier,
)
from pygame_gui.draw import draw_rectangle, draw_string, draw_text
from pygame_gui.panel import Panel


class MessageBox(Panel):
    """The 'MessageBox' class."""

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        title: str,
        message_texts: list[str] | None = None,
        button_texts: list[str] | None = None,
        callback: Callable[[str], None] | None = None,
        center: bool = True,
    ) -> None:
        """Initialises the MessageBox."""

        super().__init__(position, size, True, False)

        # Save parameters.

        self._title: str = title
        self._message_texts: list[str] | None = message_texts
        self._button_texts: list[str] | None = button_texts
        self._callback: Callable[[str], None] | None = callback
        self._center: bool = center

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # Frame style modifier can be DEFAULT only.

        self._control_type: ControlType = ControlType.MESSAGEBOX
        self._style: Style = Style.DEFAULT
        self._style_modifier: StyleModifier = StyleModifier.DEFAULT

        # Initialise other internals.

        self._showing: bool = False
        self._selection: int = -1

        # Draw titlebar, text and create the buttons.

        self.create_buttons()

    # PROPERTIES
    #   - style

    @property
    def style(self) -> Style:
        """Returns '_style'."""

        # This is overridden from the Frame superclass
        # because we need to update the title bar and buttons
        # rather than the Frame super class.

        return self._style

    @style.setter
    def style(self, new_style: Style) -> None:
        """Sets '_style'."""

        # This is overridden from the Frame superclass
        # because we need to update the title bar and buttons
        # rather than the Frame super class.

        self._style = new_style
        for _button in self._buttons:
            _button.style = new_style

    # GAME LOOP FUNCTIONS
    #   - render

    def render(self, surface: Surface) -> None:
        """Renders the Button control."""

        # Since this control is floating check that it fits
        # and adjuist the position accordingly.

        if self._center:
            self.adjust_position_to_center()

        # Allow superclass to render background and frame.

        super().render(surface)

        # Draw the message box.

        if self.showing:
            self.draw_title_bar(
                surface, self.colors["border"], self.colors["foreground"], self._title
            )
            self.draw_text_block(
                surface, self.colors["foreground"], self._message_texts
            )

    # HELPER FUNCTIONS.
    #   - adjust_position_to_center
    #   - draw_title_bar
    #   - draw_text_block
    #   - create_buttons
    #   - button_clicked

    def adjust_position_to_center(self) -> None:
        """Adjusts the position of the panel to center in the app window."""

        _window: Surface = display.get_surface()
        _x_pos: int = int((_window.get_size()[0] - self._size[0]) / 2)
        _y_pos: int = int((_window.get_size()[1] - self._size[1]) / 2)

        self._position = (_x_pos, _y_pos)

    def draw_title_bar(
        self,
        surface: Surface,
        border_color: str | None,
        text_color: str | None,
        title: str | None,
    ) -> None:
        """Draws the title bar."""

        if border_color and text_color and title:

            if not self.style_modifier == StyleModifier.OUTLINE:
                draw_rectangle(
                    surface,
                    (
                        self.get_absolute_coordinates()[0],
                        self.get_absolute_coordinates()[1],
                    ),
                    (self.size[0], DEFAULT_MESSAGEBOX_BARHEIGHT),
                    border_color,
                    self.border,
                )

            draw_string(
                surface,
                self.get_absolute_coordinates(),
                (self.size[0], DEFAULT_MESSAGEBOX_BARHEIGHT),
                text_color,
                Alignment.CENTER,
                self.font,
                title,
            )

    def draw_text_block(
        self, surface: Surface, text_color: str | None, texts: list[str] | None
    ) -> None:
        """Draws the text block."""

        if text_color and texts:
            draw_text(
                surface,
                (
                    self.get_absolute_coordinates()[0],
                    self.get_absolute_coordinates()[1]
                    + DEFAULT_MESSAGEBOX_BARHEIGHT
                    + DEFAULT_MESSAGEBOX_VERTICALPADDING,
                ),
                self.size,
                text_color,
                Alignment.CENTER,
                self.font,
                texts,
            )

    def create_buttons(self) -> None:
        """Creates the buttons."""

        self._buttons: list[Button] = []

        if self._button_texts:

            # Calculate postiion of first button.

            _total_button_width: int = len(self._button_texts) * (
                100 + DEFAULT_MESSAGEBOX_BUTTONSPACING
            )
            _x_pos: int = int((self._size[0] - _total_button_width) / 2)

            # Draw the buttons.

            for _index, _button_text in enumerate(self._button_texts):

                _position: tuple[int, int] = (
                    _x_pos,
                    self._size[1] - DEFAULT_MESSAGEBOX_SPACEFROMBOTTOM,
                )
                _button: Button = Button(
                    self,
                    _position,
                    (DEFAULT_MESSAGEBOX_BUTTONWIDTH, DEFAULT_MESSAGEBOX_BUTTONHEIGHT),
                    text=_button_text,
                    callback=partial(self.button_clicked, _button_text),
                )
                self._buttons.append(_button)

                _x_pos += (
                    DEFAULT_MESSAGEBOX_BUTTONWIDTH + DEFAULT_MESSAGEBOX_BUTTONSPACING
                )

    def button_clicked(self, text: str) -> None:
        """Callback for button clicks."""

        if self._callback:
            for _button in self._buttons:
                _button.focussed = False
                _button.selected = False
            self._callback(text)

        self._showing = False
