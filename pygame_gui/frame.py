"""
The 'frame' module defines the 'Frame' class.
"""

# Because pygame has no stub files.
# pylint: disable=no-member, no-name-in-module

# Because we want them:
# pylint: disable=too-many-instance-attributes

from __future__ import annotations

from pygame import Rect, Surface, font

from pygame_gui.constants import (
    DEFAULT_FRAME_BORDER_WIDTH,
    DEFAULT_FRAME_SELECTION_INDICATOR_INSET,
    Alignment,
    ControlType,
    Size,
    Style,
    StyleModifier,
)
from pygame_gui.control import Control
from pygame_gui.draw import draw_rectangle, draw_string
from pygame_gui.font import fonts
from pygame_gui.theme import colors_for


class Frame(Control):
    """The 'Frame' class."""

    def __init__(
        self,
        parent: Control | None,
        position: tuple[int, int],
        size: tuple[int, int],
        caption: str | None = None,
    ) -> None:

        # Initialise superclass.

        super().__init__(parent, position, size)

        # Set initial values.

        # The caption appears on the top border of the frame when provided.

        self._caption: str | None = caption

        # The control type is used to select appropriate colours for the style.
        # Example styles: DEFAULT, PRIMARY, SECONDARY, etc. see constants.py
        # Frame style modifiers can be DEFAULT or OUTLINE only.

        self._control_type: ControlType = ControlType.FRAME
        self._style: Style = Style.DEFAULT
        self._style_modifier: StyleModifier = StyleModifier.DEFAULT

        # Set the font. This will become the default for all controls
        # that subclass the Frame.

        self._font: font.Font = fonts["default"].for_size[Size.NORMAL]

        # The colors will be retreived from the themes module.

        self._colors: dict[str, str | None] = {}

        # The border determines the 'roundness' of the frame 'corners'.

        self._border: tuple[int, int, int, int] = (0, 0, 0, 0)
        self._no_border: bool = False

    # PROPERTIES.
    #   - caption
    #   - font
    #   - style
    #   - style_modifier
    #   - color
    #   - border
    #   - no_border

    @property
    def caption(self) -> str | None:
        """Returns '_caption'."""
        return self._caption

    @caption.setter
    def caption(self, new_caption: str | None) -> None:
        """Sets '_caption'."""
        self._caption = new_caption

    @property
    def font(self) -> font.Font:
        """Returns '_font'."""
        return self._font

    @font.setter
    def font(self, new_font: font.Font) -> None:
        """Sets '_font'."""
        self._font = new_font

    @property
    def style(self) -> Style:
        """Returns '_style'."""

        # This will be overriden in some classes, such as
        # MessageBox and ColorPicker, and by the ListBox,
        # because they have to manage the style of their children.

        return self._style

    @style.setter
    def style(self, new_style: Style) -> None:
        """Sets '_style'."""

        # This will be overriden in some classes, such as
        # MessageBox and ColorPicker, and by the ListBox,
        # because they have to manage the style of their children.

        self._style = new_style

    @property
    def style_modifier(self) -> StyleModifier:
        """Returns '_style_modifier'."""

        # This will be overriden in some classes, such as the ListBox,
        # because they have to manage the style of their children.

        return self._style_modifier

    @style_modifier.setter
    def style_modifier(self, new_style_modifier: StyleModifier) -> None:
        """Sets '_style_modifier'."""

        # This will be overriden in some classes, such as the ListBox,
        # because they have to manage the style of their children.

        self._style_modifier = new_style_modifier

    @property
    def colors(self) -> dict[str, str | None]:
        """Returns '_colors'."""

        # If colors have been explicitly set for this control then
        # return them, otherwise get colors from the theme.

        if self._colors:
            return self._colors
        return colors_for(
            self._control_type,
            self.style,
            self.style_modifier,
            self.focussed | self.selected,
        )

    @colors.setter
    def colors(self, new_colors: dict[str, str | None]) -> None:
        """Sets '_colors'."""
        self._colors = new_colors

    @property
    def border(self) -> tuple[int, int, int, int]:
        """Returns '_border'."""
        return self._border

    @border.setter
    def border(self, new_border: tuple[int, int, int, int]) -> None:
        """Sets '_border'."""
        self._border = new_border

    @property
    def no_border(self) -> bool:
        """Returns '_no_border'."""
        return self._no_border

    @no_border.setter
    def no_border(self, new_no_border: bool) -> None:
        """Sets '_no_border'."""
        self._no_border = new_no_border

    # GAME LOOP FUNCTIONS.
    #   - render

    def render(self, surface: Surface) -> None:
        """Renders the frame."""

        # Draw the background and frame

        self.draw_background(surface, self.colors["background"])

        if not self._no_border:
            self.draw_boarder(surface, self.colors["border"])

        if self.caption:
            self.draw_caption(surface, self.caption)

        # Children are rendered in reverse order, so that the last created
        # child will be 'on top.'

        _children: list[Control] = list(reversed(self._children))

        for _child in _children:
            _child.render(surface)

    # HELPER FUNCTIONS.
    #   - draw_background
    #   - draw_foreground
    #   - draw_selection_indicator
    #   - draw_caption

    def draw_background(self, surface: Surface, color: str | None) -> None:
        """Draws the background rectangle."""

        if color:
            draw_rectangle(
                surface,
                (
                    self.get_absolute_coordinates()[0],
                    self.get_absolute_coordinates()[1],
                ),
                self.size,
                color,
                self.border,
            )

    def draw_boarder(self, surface: Surface, color: str | None) -> None:
        """Draws the foreground rectangle."""

        if color:
            draw_rectangle(
                surface,
                (
                    self.get_absolute_coordinates()[0],
                    self.get_absolute_coordinates()[1],
                ),
                self.size,
                color,
                self.border,
                DEFAULT_FRAME_BORDER_WIDTH,
            )

    def draw_selection_indicator(self, surface: Surface, color: str | None) -> None:
        """Draws the selection indicator."""

        if color:
            draw_rectangle(
                surface,
                (
                    self.get_absolute_coordinates()[0],
                    self.get_absolute_coordinates()[1],
                ),
                self.size,
                color,
                self.border,
                DEFAULT_FRAME_BORDER_WIDTH,
                DEFAULT_FRAME_SELECTION_INDICATOR_INSET,
            )

    def draw_caption(self, surface: Surface, caption: str) -> None:
        """Draws the caption."""

        if (
            self.colors["background"]
            and self.colors["border"]
            and self.colors["foreground"]
        ):

            # Set the position of the caption.

            _x: int = self.get_absolute_coordinates()[0] + 5
            _y: int = self.get_absolute_coordinates()[1]

            # Create the text surface

            _text_surface: Surface = self.font.render(
                self.caption, True, self.colors["foreground"]
            )

            # Create a rectangle sized to the text.

            _width, _height = _text_surface.get_size()

            _y = _y - round(_height / 2)

            _rect = Rect(
                _x,
                _y,
                _width,
                _height,
            )

            # draw the caption rectangle and text.

            draw_rectangle(
                surface,
                (_x, _y),
                (_width + 10, _height + 1),
                self.colors["background"],
                self.border,
            )

            draw_rectangle(
                surface,
                (_x, _y),
                (_width + 10, _height + 1),
                self.colors["border"],
                self.border,
                DEFAULT_FRAME_BORDER_WIDTH,
            )

            draw_string(
                surface,
                (_x, _y),
                (_width + 10, _height + 1),
                self.colors["foreground"],
                Alignment.LEFT,
                self.font,
                caption,
            )
