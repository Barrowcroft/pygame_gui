"""
The 'color_picker' module defines the 'ColorPicker' class.
"""

# Because pygame has no stub files.
# pylint: disable=no-member, no-name-in-module
# pyright: reportUnknownMemberType=false
# pyright: reportAttributeAccessIssue=false

from __future__ import annotations

import colorsys
from typing import Callable

from pygame import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    Rect,
    Surface,
    display,
    draw,
    event,
    mouse,
)

from pygame_gui.button import Button
from pygame_gui.constants import (
    DEFAULT_MESSAGEBOX_BARHEIGHT,
    Alignment,
    ControlType,
    Style,
    StyleModifier,
)
from pygame_gui.draw import draw_rectangle, draw_string
from pygame_gui.panel import Panel

# Because we want them:
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


class ColorPicker(Panel):
    """The 'ColorPicker' class."""

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        callback: Callable[[str], None] | None = None,
        center: bool = True,
    ) -> None:
        """Initialises the ColorPicker."""

        super().__init__(position, size, True, False)

        # Save parameters.

        self._title: str = "Color Picker"
        self._callback: Callable[[str], None] | None = callback
        self._center: bool = center

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # Frame style modifier can be DEFAULT only.

        self._control_type: ControlType = ControlType.COLORPICKER
        self._style: Style = Style.DEFAULT
        self._style_modifier: StyleModifier = StyleModifier.DEFAULT

        # Initialise other internals.

        self._showing: bool = False
        self._selection: int = -1
        self._dragging: bool = False

        # Initialise the HS, brightness and swatch rectangles.

        self._hs_rect = Rect(
            self.get_absolute_coordinates()[0] + 10,
            self.get_absolute_coordinates()[0] + 40,
            150,
            150,
        )
        self._v_rect = Rect(
            self.get_absolute_coordinates()[0] + 170,
            self.get_absolute_coordinates()[1] + 40,
            30,
            150,
        )
        self._swatch_rect = Rect(
            self.get_absolute_coordinates()[0] + 220,
            self.get_absolute_coordinates()[1] + 40,
            60,
            60,
        )

        # Initialise color values.

        self._current_h: int = 0
        self._current_s: int = 1
        self._current_v: int = 1
        self._picked_color: str = "#FF0000"

        # Draw titlebar, text and create the buttons.

        self.create_button()

    # PROPERTIES
    #   - style
    #   - picked_color

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
        self._ok_button.style = new_style

    @property
    def picked_color(self) -> str:
        """Returns '_picked_color'."""
        return self._picked_color

    @picked_color.setter
    def picked_color(self, new_picked_color: str) -> None:
        """Sets '_picked_color'."""
        self._picked_color = new_picked_color

    # GAME LOOP FUNCTIONS

    def handle_mouse_event(self, event_to_handle: event.Event) -> bool:
        """Handles mouse events.
        Returning True indicates that the event has been exhaustively dealt
        with and that no futher Frames should be given the opportunity
        to repsond to the event."""

        _event_handled: bool = super().handle_mouse_event(event_to_handle)

        # Dont handle events if not showing.

        if self._showing:

            # # If the panel has focus it will consume all events.

            # if self.focussed:
            #     _event_handled = True

            # # If the panel is modal it will consume all events,
            # # even if it doesn't have focus.

            # if self._modal:
            #     _event_handled = True

            # # If the panel is supposed to close on lost focus then close it.

            # if not self.focussed and self._close_on_lost_focus:
            #     self._showing = False

            # If mouse button pressed then we are dragging:

            if event_to_handle.type == MOUSEBUTTONDOWN:
                self._dragging = True

            if event_to_handle.type == MOUSEBUTTONUP:
                self._dragging = False

            if self._dragging:
                mx, my = mouse.get_pos()

                _collide: bool = False

                if self._hs_rect.collidepoint((mx, my)):
                    self._current_h, self._current_s = self.get_hs_at((mx, my))
                    _collide = True
                if self._v_rect.collidepoint((mx, my)):
                    self._current_v = self.get_brightness_at((mx, my))
                    _collide = True

                if _collide:
                    self._picked_color = self.hsv_to_hex(
                        self._current_h, self._current_s, self._current_v
                    )

        return _event_handled

    def render(self, surface: Surface) -> None:
        """Renders the Button control."""

        # Since this control is floating check that it fits
        # and adjuist the position accordingly.

        if self._center:
            self.adjust_position_to_center()

        # Allow superclass to render background and frame.

        super().render(surface)

        # Draw the color picker.

        if self.showing:
            self.draw_title_bar(
                surface, self.colors["border"], self.colors["foreground"], self._title
            )

            self.draw_hs_square(surface)
            self.draw_brightness_rect(surface)
            self.draw_swatch(surface)
            self.draw_labels(surface, self.colors["border"])

    # HELPER FUNCTIONS.
    #   - adjust_position_to_center
    #   - draw_title_bar
    #   - draw_labels
    #   - draw_hs_square
    #   - draw_brightness_rect
    #   - draw_swatch
    #   - get_hs_at
    #   - get_brightness_at
    #   - hsv_to_hex
    #   - create_button
    #   - button_clicked

    def adjust_position_to_center(self) -> None:
        """Adjusts the position of the panel to center in the app window."""

        _window: Surface = display.get_surface()
        _x_pos: int = int((_window.get_size()[0] - self._size[0]) / 2)
        _y_pos: int = int((_window.get_size()[1] - self._size[1]) / 2)

        self._position = (_x_pos, _y_pos)

        self._hs_rect = Rect(
            self.get_absolute_coordinates()[0] + 10,
            self.get_absolute_coordinates()[1] + 40,
            150,
            150,
        )  # Hue/Saturation square
        self._v_rect = Rect(
            self.get_absolute_coordinates()[0] + 170,
            self.get_absolute_coordinates()[1] + 40,
            30,
            150,
        )  # Brightness slider
        self._swatch_rect = Rect(
            self.get_absolute_coordinates()[0] + 210,
            self.get_absolute_coordinates()[1] + 40,
            60,
            60,
        )  # Swatch

    def draw_title_bar(
        self,
        surface: Surface,
        border_color: str | None,
        text_color: str | None,
        title: str | None,
    ) -> None:
        """Draws the title bar."""

        if border_color and text_color and title:

            if self.style_modifier != StyleModifier.OUTLINE:
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

    def draw_labels(self, surface: Surface, color: str | None) -> None:
        """Draws the labels."""

        if color:
            draw_string(
                surface,
                (
                    self.get_absolute_coordinates()[0] + 270,
                    self.get_absolute_coordinates()[1] + 31,
                ),
                (100, 30),
                color,
                Alignment.LEFT,
                self.font,
                f"R: #{self.picked_color[1:3].upper()}",
            )
            draw_string(
                surface,
                (
                    self.get_absolute_coordinates()[0] + 270,
                    self.get_absolute_coordinates()[1] + 55,
                ),
                (100, 30),
                color,
                Alignment.LEFT,
                self.font,
                f"G: #{self.picked_color[3:5].upper()}",
            )
            draw_string(
                surface,
                (
                    self.get_absolute_coordinates()[0] + 270,
                    self.get_absolute_coordinates()[1] + 79,
                ),
                (100, 30),
                color,
                Alignment.LEFT,
                self.font,
                f"B: #{self.picked_color[5:7].upper()}",
            )

    def draw_hs_square(self, surface: Surface):
        """Draw hue/saturation square."""
        for x in range(self._hs_rect.w):
            for y in range(self._hs_rect.h):
                h = x / self._hs_rect.w
                s = 1 - (y / self._hs_rect.h)
                r, g, b = colorsys.hsv_to_rgb(h, s, self._current_v)
                surface.set_at(
                    (
                        self._hs_rect.x + x,
                        self._hs_rect.y + y,
                    ),
                    (int(r * 255), int(g * 255), int(b * 255)),
                )

    def draw_brightness_rect(self, surface: Surface):
        """Draw brightness slider."""
        for y in range(self._v_rect.h):
            v = 1 - (y / self._v_rect.h)
            r, g, b = colorsys.hsv_to_rgb(self._current_h, self._current_s, v)
            draw.line(
                surface,
                (int(r * 255), int(g * 255), int(b * 255)),
                (
                    self._v_rect.x,
                    self._v_rect.y + y,
                ),
                (
                    self._v_rect.x + self._v_rect.w,
                    self._v_rect.y + y,
                ),
            )

    def draw_swatch(self, surface: Surface) -> None:
        """Draws the swatch."""

        draw.rect(surface, self._picked_color, self._swatch_rect)

    def get_hs_at(self, pos: tuple[int, int]) -> tuple[float, float]:
        """Return (h, s) based on mouse coords."""
        x, y = pos
        h = (x - self._hs_rect.x) / self._hs_rect.w
        s = 1 - ((y - self._hs_rect.y) / self._hs_rect.h)
        return max(0, min(h, 1)), max(0, min(s, 1))

    def get_brightness_at(self, pos: tuple[int, int]) -> float:
        """Return brightness value based on slider."""
        _, y = pos
        v = 1 - ((y - self._v_rect.y) / self._v_rect.h)
        return max(0, min(v, 1))

    def hsv_to_hex(self, h: int, s: int, v: int) -> str:
        """Convert h,s,b to hex"""
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    def create_button(self) -> None:
        """Creates the button."""

        self._ok_button: Button = Button(
            self, (210, 160), (110, 30), "Done", self.button_clicked
        )

    def button_clicked(self) -> None:
        """Callback for button clicks."""

        if self._callback:
            self._callback(self._picked_color)

        self._showing = False
