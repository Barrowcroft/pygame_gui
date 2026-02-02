"""The 'constants' module define all the shared constants and enums."""

from enum import Enum, auto

# ENUMERATORS.


class ControlType(Enum):
    """The 'ControlType' enum"""

    CONTROL = auto()
    FRAME = auto()
    LABEL = auto()
    TEXTBLOCK = auto()
    BUTTON = auto()
    TOGGLEBUTTON = auto()
    TOGGLESWITCH = auto()
    TOGGLESWITCHROUNDEL = auto()
    RADIOBUTTON = auto()
    RADIOSWITCH = auto()
    RADIOSWITCHROUNDEL = auto()
    LISTBOX = auto()
    LISTBOXITEM = auto()
    ENTRYBOX = auto()
    PANEL = auto()
    MESSAGEBOX = auto()
    COLORPICKER = auto()
    PROGRESSBAR = auto()
    ROUNDEL = auto()
    SLIDER = auto()
    MENUBUTTON = auto()
    MENU = auto()


class Style(Enum):
    """The 'Style' enum."""

    DEFAULT = "default"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"
    LIGHT = "light"
    DARK = "dark"


class StyleModifier(Enum):
    """The 'StyleModifier' enum."""

    DEFAULT = auto()
    OUTLINE = auto()
    INVERSE = auto()
    SIMPLE = auto()


class Alignment(Enum):
    """The 'Alignment' enum."""

    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()
    CENTER = auto()


class Size(Enum):
    """The 'Size' enum."""

    VERYSMALL = auto()
    SMALL = auto()
    NORMAL = auto()
    LARGE = auto()
    VERYLARGE = auto()


# LAYOUT CONSTANTS

DEFAULT_FRAME_BORDER_WIDTH = 1
DEFAULT_FRAME_SELECTION_INDICATOR_INSET = 2

DEFAULT_TEXT_HORIZONTAL_PADDING = 5
DEFAULT_TEXT_VERTICAL_PADDING = 5

DEFAULT_SWITCH_ROUNDEL_RADIUS = 15

DEFAULT_MESSAGEBOX_BARHEIGHT = 30
DEFAULT_MESSAGEBOX_BUTTONHEIGHT = 30
DEFAULT_MESSAGEBOX_BUTTONSPACING = 5
DEFAULT_MESSAGEBOX_BUTTONWIDTH = 100
DEFAULT_MESSAGEBOX_HORIZONTALPADDING = 10
DEFAULT_MESSAGEBOX_SPACEFROMBOTTOM = 40
DEFAULT_MESSAGEBOX_VERTICALPADDING = 10

DEFAULT_PANEL_SHADOW_COLOR = "#323232"


DEFAULT_MENUBUTTON_TOPPADDING = 0
DEFAULT_MENUBUTTON_ITEMPADDING = 0

DEFAULT_MENU_ITEM_HEIGHT = 25
