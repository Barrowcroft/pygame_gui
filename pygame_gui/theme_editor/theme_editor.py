"""Test app."""

# Because pygame has no stub files.
# pylint: disable=no-member, no-name-in-module
# pylint: disable=too-many-instance-attributes

# Because we want them:
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-public-methods

from functools import partial

import pygame

from pygame_gui.button import Button
from pygame_gui.color_picker import ColorPicker
from pygame_gui.constants import Alignment, Style, StyleModifier
from pygame_gui.entry_box import EntryBox
from pygame_gui.frame import Frame
from pygame_gui.label import Label
from pygame_gui.list_box import ListBox
from pygame_gui.menu_button import MenuButton
from pygame_gui.message_box import MessageBox
from pygame_gui.progress_bar import ProgressBar
from pygame_gui.radio_button import RadioButton
from pygame_gui.radio_switch import RadioSwitch
from pygame_gui.selection_box import SelectionBox
from pygame_gui.slider import Slider
from pygame_gui.text_block import TextBlock
from pygame_gui.theme import new_theme, rename_theme, set_theme, themes
from pygame_gui.toggle_button import ToggleButton
from pygame_gui.toggle_switch import ToggleSwitch


class App:
    """Main App."""

    def __init__(self) -> None:

        # Initialise pygame.

        pygame.init()

        # Create a window

        self._screen = pygame.display.set_mode((1080, 645))
        pygame.display.set_caption("pygame_gui example")

        # Initialise theme ans styles.

        self._current_theme: str = "solar"
        set_theme(self._current_theme)

        self._current_style: Style = Style.PRIMARY

        self._theme_names = [theme for theme in themes.keys()]

        self._frame_style: Style = Style.DEFAULT
        self._control_style: Style = Style.PRIMARY

        # Create master frame

        self._master: Frame = Frame(None, (10, 10), (1060, 625))
        self._master.style = Style.SECONDARY
        self._master.no_border = True

        self.draw_styles(220, 10)
        self.draw_labels(220, 75)
        self.draw_text_blocks(430, 75)
        self.draw_buttons(640, 75)
        self.draw_toggle_buttons(850, 75)
        self.draw_radio_buttons(220, 240)
        self.draw_list_box_1(430, 240)
        self.draw_list_box_2(640, 240)
        self.draw_entry_box(850, 240)
        self.draw_message_box_button(220, 405)
        self.draw_progress_bars_and_slider(430, 405)
        self.draw_toggle_switches(640, 405)
        self.draw_radio_switches(850, 405)

        self._swatches: list[Button] = []
        self.draw_color_palette(10, 10)
        self.draw_status_panel(220, 565)

        # Create message box and color picker.

        self._message_box: MessageBox = MessageBox(
            (10, 10),
            (400, 200),
            "This is a message",
            [
                "This is a message box",
                "You can have as many lines of text as you like",
                "and as many buttons as you want",
                "but you must make sure",
                "you size the message box to fit",
            ],
            ["Yes", "No", "Quit"],
            self.message_box_closed,
        )
        self._message_box.style = Style.PRIMARY
        self._message_box.style_modifier = StyleModifier.DEFAULT
        self._message_box.showing = False

        self._color_picker: ColorPicker = ColorPicker(
            (10, 10),
            (330, 200),
            self.color_picker_closed,
        )
        self._color_picker.style = Style.PRIMARY
        self._color_picker.style_modifier = StyleModifier.DEFAULT
        self._color_picker.showing = False
        self._color_picked_for: str = ""

    def render(self, screen: pygame.Surface) -> None:
        """Renders the controls."""

        screen.fill((0, 0, 0, 1))

        self._master.render(screen)
        self._message_box.render(screen)
        self._color_picker.render(screen)

        self._menu_buton_1.render_menu(screen)
        self._selection_box_8_1.render_menu(screen)

        # Update the display

        pygame.display.flip()

    def run(self) -> None:
        """Main."""

        # Main loop

        _running: bool = True

        while _running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    _running = False

                if event.type == pygame.KEYDOWN:
                    self._master.handle_key_event(event)

                if (
                    event.type
                    in (
                        pygame.MOUSEBUTTONDOWN,
                        pygame.MOUSEBUTTONUP,
                        pygame.MOUSEMOTION,
                    )
                    and (
                        not self._message_box.showing
                        or not self._message_box.handle_mouse_event(event)
                    )
                    and (
                        not self._color_picker.showing
                        or not self._color_picker.handle_mouse_event(event)
                    )
                    and (
                        not self._menu_buton_1.menu.showing
                        or not self._menu_buton_1.menu.handle_mouse_event(event)
                    )
                    and (
                        not self._selection_box_8_1.menu.showing
                        or not self._selection_box_8_1.menu.handle_mouse_event(event)
                    )
                ):
                    self._master.handle_mouse_event(event)

                self._master.update(0)  # set delta time to zero for now.
                self._menu_buton_1.menu.update(0)

                self.render(self._screen)

        # Quit Pygame

        pygame.quit()

    def draw_color_palette(self, x: int, y: int) -> None:
        """Draws the color palette."""

        self._palette: list[str] = [
            "default",
            "primary",
            "secondary",
            "success",
            "info",
            "warning",
            "danger",
            "light",
            "dark",
            "foreground",
        ]

        self._frame: Frame = Frame(self._master, (x, y), (200, 605), "Palette")
        self._frame.style = self._frame_style
        self._frame.style_modifier = StyleModifier.DEFAULT

        _x: int = 10
        _y: int = 15

        _frame: Frame = self._frame
        _style: Style = self._control_style

        self._menu_buton_1: MenuButton = MenuButton(
            _frame, (_x, _y), (180, 30), self.menu_button_callback, self._theme_names
        )
        self._menu_buton_1.style = _style
        self._menu_buton_1.style_modifier = StyleModifier.DEFAULT

        _y += 40

        self._entry_box_1: EntryBox = EntryBox(
            self._frame,
            (_x, _y),
            (180, 30),
            "New Theme",
            callback_on_change=self.entry_box_changed,
            callback_on_exit=self.theme_entry_box_exit,
        )
        self._entry_box_1.style = Style.PRIMARY
        self._entry_box_1.style_modifier = StyleModifier.DEFAULT

        _y += 50

        self.draw_swatches(_frame, self._palette)

        self._labels: list[Label] = []

        for _color in self._palette:

            _label: Label = Label(_frame, (_x, _y), (180, 30), _color)
            _label.style = _style
            _label.style_modifier = StyleModifier.OUTLINE

            self._labels.append(_label)

            _y += 40

    def draw_swatches(self, frame: Frame, palette: list[str]) -> None:
        """Draws the swatches."""

        _y: int = 105

        if not self._swatches:
            for _color in palette:
                _button: Button = Button(
                    frame,
                    (150, _y),
                    (40, 30),
                    "",
                    partial(self.open_color_picker, _color),
                )
                _button.style = Style.PRIMARY
                _button.style_modifier = StyleModifier.OUTLINE
                _button.colors = {
                    "background": themes[self._current_theme]["colors"][_color],
                    "border": themes[self._current_theme]["colors"][
                        self._control_style.value
                    ],
                    "selection": None,
                    "foreground": None,
                }
                self._swatches.append(_button)
                _y += 40
        else:
            for _button, _color in zip(self._swatches, self._palette):
                _button.colors = {
                    "background": themes[self._current_theme]["colors"][_color],
                    "border": themes[self._current_theme]["colors"][
                        self._control_style.value
                    ],
                    "selection": None,
                    "foreground": None,
                }

    def draw_styles(self, x: int, y: int) -> None:
        """Draws the styles."""

        self._frame_0: Frame = Frame(self._master, (x, y), (830, 50))
        self._frame_0.style = self._frame_style
        self._frame_0.style_modifier = StyleModifier.DEFAULT

        _x: int = 10
        _y: int = 10

        for _style in Style:
            self._button: Button = Button(
                self._frame_0,
                (_x, _y),
                (85, 30),
                _style.value,
                partial(self.change_style, _style),
            )
            self._button.style = _style
            _x += 90

    def draw_labels(self, x: int, y: int) -> None:
        "Draws the labels."

        self._frame_1: Frame = Frame(self._master, (x, y), (200, 150))
        self._frame_1.style = self._frame_style
        self._frame_1.style_modifier = StyleModifier.DEFAULT
        self._frame_1.caption = "Label"

        _frame: Frame = self._frame_1
        _style: Style = self._control_style

        _x: int = 10
        _y: int = 15

        self._label_1_1: Label = Label(_frame, (_x, _y), (180, 30), "Default")
        self._label_1_1.style = _style
        self._label_1_1.style_modifier = StyleModifier.DEFAULT

        _y += 35

        self._label_1_2: Label = Label(_frame, (_x, _y), (180, 30), "Outline")
        self._label_1_2.style = _style
        self._label_1_2.style_modifier = StyleModifier.OUTLINE

        _y += 40

        self._label_1_3: Label = Label(_frame, (_x, _y), (180, 30), "Inverse")
        self._label_1_3.style = _style
        self._label_1_3.style_modifier = StyleModifier.INVERSE

    def draw_text_blocks(self, x: int, y: int) -> None:
        """Draws the text blocks."""

        self._frame_2: Frame = Frame(self._master, (x, y), (200, 150))
        self._frame_2.style = self._frame_style
        self._frame_2.style_modifier = StyleModifier.DEFAULT
        self._frame_2.caption = "TextBlock"

        _frame: Frame = self._frame_2
        _style: Style = self._control_style

        _x: int = 10
        _y: int = 15

        self._text_block_2_1: TextBlock = TextBlock(
            self._frame_2,
            (_x, _y),
            (180, 60),
            [
                "This is the first line of text.",
                "This is the second,",
                "and this is the third.",
            ],
        )
        self._text_block_2_1.style = _style
        self._text_block_2_1.style_modifier = StyleModifier.DEFAULT
        self._text_block_2_1.alignment = Alignment.CENTER

        _y += 65

        self._text_block_2_2: TextBlock = TextBlock(
            self._frame_2,
            (_x, _y),
            (180, 60),
            [
                "Text blocks can also",
                "use OUTLINE and",
                "INVERSE styles.",
            ],
        )
        self._text_block_2_2.style = _style
        self._text_block_2_2.style_modifier = StyleModifier.INVERSE
        self._text_block_2_2.alignment = Alignment.CENTER

    def draw_buttons(self, x: int, y: int) -> None:
        """Draws the buttons."""

        self._frame_3: Frame = Frame(self._master, (x, y), (200, 150))
        self._frame_3.style = self._frame_style
        self._frame_3.style_modifier = StyleModifier.DEFAULT
        self._frame_3.caption = "Button"

        _frame: Frame = self._frame_3
        _style: Style = self._control_style

        _x: int = 10
        _y: int = 20

        self._buton_3_1: Button = Button(
            _frame,
            (_x, _y),
            (180, 30),
            "Default",
            partial(self.button_callback, "Button 01"),
        )
        self._buton_3_1.style = _style
        self._buton_3_1.style_modifier = StyleModifier.DEFAULT

        _y += 40

        self._buton_3_2: Button = Button(
            _frame,
            (_x, _y),
            (180, 30),
            "Outline",
            partial(self.button_callback, "Button 02"),
        )
        self._buton_3_2.style = _style
        self._buton_3_2.style_modifier = StyleModifier.OUTLINE

        _y += 40

        self._buton_3_3: Button = Button(
            _frame,
            (_x, _y),
            (180, 30),
            "Simple",
            partial(self.button_callback, "Button 03"),
        )
        self._buton_3_3.style = _style
        self._buton_3_3.style_modifier = StyleModifier.SIMPLE

    def draw_toggle_buttons(self, x: int, y: int) -> None:
        """Draws the toggle buttons."""

        self._frame_4: Frame = Frame(self._master, (x, y), (200, 150))
        self._frame_4.style = self._frame_style
        self._frame_4.style_modifier = StyleModifier.DEFAULT
        self._frame_4.caption = "ToggleButton"

        _frame: Frame = self._frame_4
        _style: Style = self._control_style

        _x: int = 10
        _y: int = 20

        self._buton_4_1: ToggleButton = ToggleButton(
            _frame,
            (_x, _y),
            (180, 30),
            "ToggleButton",
            partial(self.button_callback, "Toggle Button 01"),
        )

        self._buton_4_1.style = _style
        self._buton_4_1.style_modifier = StyleModifier.DEFAULT

        _y += 40

        self._buton_4_2: ToggleButton = ToggleButton(
            _frame,
            (_x, _y),
            (180, 30),
            "ToggleButton",
            partial(self.button_callback, "Toggle Button 02"),
        )
        self._buton_4_2.style = _style
        self._buton_4_2.style_modifier = StyleModifier.DEFAULT

        _y += 40

        self._buton_4_3: ToggleButton = ToggleButton(
            _frame,
            (_x, _y),
            (180, 30),
            "ToggleButton",
            partial(self.button_callback, "Toggle Button 03"),
        )
        self._buton_4_3.style = _style
        self._buton_4_3.style_modifier = StyleModifier.DEFAULT

    def draw_radio_buttons(self, x: int, y: int) -> None:
        """Draws the radio buttons."""

        self._frame_5: Frame = Frame(self._master, (x, y), (200, 150))
        self._frame_5.style = self._frame_style
        self._frame_5.style_modifier = StyleModifier.DEFAULT
        self._frame_5.caption = "RadioButton"

        _frame: Frame = self._frame_5
        _style: Style = self._control_style

        _x: int = 10
        _y: int = 20

        self._buton_5_1: RadioButton = RadioButton(
            _frame,
            (_x, _y),
            (180, 30),
            "RadioButon",
            partial(self.button_callback, "Radio Button 01"),
        )
        self._buton_5_1.style = _style
        self._buton_5_1.style_modifier = StyleModifier.DEFAULT

        _y += 40

        self._buton_5_2: RadioButton = RadioButton(
            _frame,
            (_x, _y),
            (180, 30),
            "RadioButon",
            partial(self.button_callback, "Radio Button 02"),
        )
        self._buton_5_2.style = _style
        self._buton_5_2.style_modifier = StyleModifier.DEFAULT

        _y += 40

        self._buton_5_3: RadioButton = RadioButton(
            _frame,
            (_x, _y),
            (180, 30),
            "RadioButon",
            partial(self.button_callback, "Radio Button 03"),
        )
        self._buton_5_3.style = _style
        self._buton_5_3.style_modifier = StyleModifier.DEFAULT

    def draw_list_box_1(self, x: int, y: int) -> None:
        """Draws the list box."""

        self._frame_6: Frame = Frame(self._master, (x, y), (200, 150))
        self._frame_6.style = self._frame_style
        self._frame_6.style_modifier = StyleModifier.DEFAULT
        self._frame_6.caption = "ListBox"

        self._list_box_6_1: ListBox = ListBox(
            self._frame_6,
            (10, 15),
            (180, 125),
            self._theme_names,
            24,
            self.change_theme,
        )
        self._list_box_6_1.style = Style.PRIMARY
        self._list_box_6_1.style_modifier = StyleModifier.DEFAULT

    def draw_list_box_2(self, x: int, y: int) -> None:
        """Draws the list box."""

        self._frame_7: Frame = Frame(self._master, (x, y), (200, 150))
        self._frame_7.style = self._frame_style
        self._frame_7.style_modifier = StyleModifier.DEFAULT
        self._frame_7.caption = "ListBox"

        _theme_names: list[str] = list(reversed(self._theme_names))

        self._list_box_7_1: ListBox = ListBox(
            self._frame_7,
            (10, 15),
            (180, 125),
            _theme_names,
            24,
            self.change_theme,
        )
        self._list_box_7_1.style = Style.PRIMARY
        self._list_box_7_1.style_modifier = StyleModifier.OUTLINE

    def draw_entry_box(self, x: int, y: int) -> None:
        """Draws the entry box."""

        self._frame_8: Frame = Frame(self._master, (x, y), (200, 150))
        self._frame_8.style = self._frame_style
        self._frame_8.style_modifier = StyleModifier.DEFAULT
        self._frame_8.caption = "EntryBox"

        _x: int = 10
        _y: int = 15

        self._entry_box_8_1: EntryBox = EntryBox(
            self._frame_8,
            (_x, _y),
            (180, 30),
            "Default",
            callback_on_change=self.entry_box_changed,
            callback_on_exit=self.entry_box_exit,
        )
        self._entry_box_8_1.style = Style.PRIMARY
        self._entry_box_8_1.style_modifier = StyleModifier.DEFAULT

        _y += 35

        self._entry_box_8_2: EntryBox = EntryBox(
            self._frame_8,
            (_x, _y),
            (180, 30),
            "Default",
            secret=True,
            callback_on_change=self.entry_box_changed,
            callback_on_exit=self.entry_box_exit,
        )
        self._entry_box_8_2.style = Style.PRIMARY
        self._entry_box_8_2.style_modifier = StyleModifier.OUTLINE

        _y += 35

        self._selection_box_8_1: SelectionBox = SelectionBox(
            self._frame_8,
            (_x, _y),
            (180, 30),
            "",
            self.entry_box_changed,
            self.entry_box_exit,
            self.entry_selected,
            ["Selection 01", "Selection 02", "Selection 03"],
        )
        self._selection_box_8_1.style = Style.PRIMARY
        self._selection_box_8_1.style_modifier = StyleModifier.OUTLINE

    def draw_status_panel(self, x: int, y: int) -> None:
        """Draws the message box."""

        self._frame_9: Frame = Frame(self._master, (x, y), (830, 50))
        self._frame_9.style = self._frame_style
        self._frame_9.style_modifier = StyleModifier.DEFAULT

        self._status_message: Label = Label(self._frame_9, (10, 10), (810, 30), "")
        self._status_message.style = self._control_style
        self._status_message.style_modifier = StyleModifier.DEFAULT

    def draw_message_box_button(self, x: int, y: int) -> None:
        """Draws the button to pop up the message box."""

        self._frame_10: Frame = Frame(self._master, (x, y), (200, 150), "MessageBox")
        self._frame_10.style = self._frame_style
        self._frame_10.style_modifier = StyleModifier.DEFAULT

        _frame: Frame = self._frame_10
        _style: Style = self._control_style

        _x: int = 10
        _y: int = 20

        self._buton_10_1: Button = Button(
            _frame,
            (_x, _y),
            (180, 30),
            "Show MessageBox",
            partial(self.button_callback, "Show MessageBox"),
        )
        self._buton_10_1.style = _style
        self._buton_10_1.style_modifier = StyleModifier.DEFAULT

    def draw_progress_bars_and_slider(self, x: int, y: int) -> None:
        """Draws the progress bars and sliders."""

        self._frame_11: Frame = Frame(
            self._master, (x, y), (200, 150), "ProgressBar/Slider"
        )
        self._frame_11.style = self._frame_style
        self._frame_11.style_modifier = StyleModifier.DEFAULT

        _frame: Frame = self._frame_11
        _style: Style = self._control_style

        _x: int = 10
        _y: int = 20

        self._progress_bar_11_1: ProgressBar = ProgressBar(
            _frame, (_x, _y), (180, 30), "Progress", 60
        )
        self._progress_bar_11_1.style = _style
        self._progress_bar_11_1.style_modifier = StyleModifier.DEFAULT

        _y += 40

        self._progress_bar_11_2: ProgressBar = ProgressBar(
            _frame, (_x, _y), (180, 30), "Progress", 60
        )
        self._progress_bar_11_2.style = _style
        self._progress_bar_11_2.style_modifier = StyleModifier.INVERSE

        _y += 40

        self._slider_11_1: Slider = Slider(
            _frame, (_x, _y), (180, 30), self.slider_moves, 60
        )
        self._slider_11_1.style = _style
        self._slider_11_1.style_modifier = StyleModifier.DEFAULT

    def draw_toggle_switches(self, x: int, y: int) -> None:
        """Draws the toggle switches."""

        self._frame_12: Frame = Frame(
            self._master, (x, y), (200, 150), "Toggle Switches"
        )
        self._frame_12.style = self._frame_style
        self._frame_12.style_modifier = StyleModifier.DEFAULT

        _frame: Frame = self._frame_12
        _style: Style = self._control_style

        _x: int = 10
        _y: int = 20

        self._buton_12_1: ToggleSwitch = ToggleSwitch(
            _frame,
            (_x, _y),
            (180, 30),
            "ToggleSwitch",
            partial(self.button_callback, "Toggle Switch 01"),
        )

        self._buton_12_1.style = _style
        self._buton_12_1.style_modifier = StyleModifier.DEFAULT

        _y += 40

        self._buton_12_2: ToggleSwitch = ToggleSwitch(
            _frame,
            (_x, _y),
            (180, 30),
            "ToggleSwitch",
            partial(self.button_callback, "Toggle Switch 02"),
        )
        self._buton_12_2.style = _style
        self._buton_12_2.style_modifier = StyleModifier.DEFAULT

        _y += 40

        self._buton_12_3: ToggleSwitch = ToggleSwitch(
            _frame,
            (_x, _y),
            (180, 30),
            "ToggleSwitch",
            partial(self.button_callback, "Toggle Switch 03"),
        )
        self._buton_12_3.style = _style
        self._buton_12_3.style_modifier = StyleModifier.DEFAULT

    def draw_radio_switches(self, x: int, y: int) -> None:
        """Draws the radio switches."""

        self._frame_13: Frame = Frame(
            self._master, (x, y), (200, 150), "Radio Switches"
        )
        self._frame_13.style = self._frame_style
        self._frame_13.style_modifier = StyleModifier.DEFAULT

        _frame: Frame = self._frame_13
        _style: Style = self._control_style

        _x: int = 10
        _y: int = 20

        self._buton_13_1: RadioSwitch = RadioSwitch(
            _frame,
            (_x, _y),
            (180, 30),
            "RadioSwitch",
            partial(self.button_callback, "Radio Switch 01"),
        )

        self._buton_13_1.style = _style
        self._buton_13_1.style_modifier = StyleModifier.DEFAULT

        _y += 40

        self._buton_13_2: RadioSwitch = RadioSwitch(
            _frame,
            (_x, _y),
            (180, 30),
            "RadioSwitch",
            partial(self.button_callback, "Radio Switch 02"),
        )
        self._buton_13_2.style = _style
        self._buton_13_2.style_modifier = StyleModifier.DEFAULT

        _y += 40

        self._buton_13_3: RadioSwitch = RadioSwitch(
            _frame,
            (_x, _y),
            (180, 30),
            "RadioSwitch",
            partial(self.button_callback, "Radio Switch 03"),
        )
        self._buton_13_3.style = _style
        self._buton_13_3.style_modifier = StyleModifier.DEFAULT

    def show_message(self, text: str) -> None:
        """Displays a message."""

        self._status_message.text = text

    def button_callback(self, text: str) -> None:
        """Button callback."""

        self.show_message(f"Button pressed - {text}")

        if text == "Show MessageBox":
            self._message_box.showing = True

    def menu_button_callback(self, selection: str) -> None:
        """Menu button callback."""

        self.change_theme(selection)
        self.show_message(f"Menu button pressed with selection - {selection}")

    def entry_box_changed(self, text: str) -> None:
        """Entry box callback."""

        self.show_message(f"Entry box changed - {text}")

    def entry_selected(self, text: str) -> None:
        """Selction box callback."""

        self.show_message(f"Entry selected - {text}")

    def entry_box_exit(self, new_theme_name: str) -> None:
        """Entry box callback."""

        self.show_message(f"Entry box exit - {new_theme_name}")

    def theme_entry_box_exit(self, new_theme_name: str) -> None:
        """Theme entry box callback."""

        rename_theme(self._current_theme, new_theme_name)
        self._current_theme = new_theme_name

        self.show_message(f"Theme entry box exit - {new_theme_name}")

    def message_box_closed(self, text: str) -> None:
        """Callback for message box."""

        self.show_message(f"Message box closed with response - {text}")

    def open_color_picker(self, color: str) -> None:
        """Opens the color picker."""

        self._color_picked_for = color
        self._color_picker.picked_color = themes[self._current_theme]["colors"][color]

        self._color_picker.showing = True

    def color_picker_closed(self, color: str) -> None:
        """Callback for color picker."""

        themes[self._current_theme]["colors"][self._color_picked_for] = color

        new_theme(self._current_theme, self._entry_box_1.value)
        self.change_theme(self._entry_box_1.value)

        self.draw_swatches(self._frame, self._palette)
        self.show_message(f"Color picker closed with color - {color}")

    def slider_moves(self, percent: int) -> None:
        """The callback fro the slider."""

        self._progress_bar_11_1.percent = percent
        self._progress_bar_11_2.percent = percent

        self.show_message(f"Slider set to {percent}%")

    def change_style(self, style: Style) -> None:
        """Button callback."""

        self.show_message(f"Changing style to - {style.value.upper()}")

        self._menu_buton_1.style = style
        self._menu_buton_1.menu.style = style

        self._entry_box_1.style = style

        for _label in self._labels:
            _label.style = style

        self._control_style = style

        self._label_1_1.style = style
        self._label_1_2.style = style
        self._label_1_3.style = style
        self._text_block_2_1.style = style
        self._text_block_2_2.style = style
        self._buton_3_1.style = style
        self._buton_3_2.style = style
        self._buton_3_3.style = style
        self._buton_4_1.style = style
        self._buton_4_2.style = style
        self._buton_4_3.style = style
        self._buton_5_1.style = style
        self._buton_5_2.style = style
        self._buton_5_3.style = style
        self._list_box_6_1.style = style
        self._list_box_7_1.style = style
        self._entry_box_8_1.style = style
        self._entry_box_8_2.style = style
        self._buton_10_1.style = style
        self._progress_bar_11_1.style = style
        self._progress_bar_11_2.style = style
        self._slider_11_1.style = style
        self._buton_12_1.style = style
        self._buton_12_2.style = style
        self._buton_12_3.style = style
        self._buton_13_1.style = style
        self._buton_13_2.style = style
        self._buton_13_3.style = style
        self._status_message.style = style
        self._message_box.style = style
        self._color_picker.style = style

        self.draw_swatches(self._frame, self._palette)

    def change_theme(self, theme: str) -> None:
        """Changes the theme."""

        self.show_message(f"Changing theme to - {theme.upper()}")
        self._current_theme: str = theme
        self._entry_box_1.value = theme

        set_theme(self._current_theme)

        self.draw_swatches(self._frame, self._palette)

    def change_color(self, color: str) -> None:
        """Changes the theme."""

        self.show_message(f"Changing color for {color}")


if __name__ == "__main__":

    _app: App = App()
    _app.run()
