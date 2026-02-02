"""
The 'theme' module defines the 'themes' dictionary,
loading themes from disk combining them into a single dictionary.
"""

# Because we want them:
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements

from pathlib import Path
from typing import Any

from pygame_gui.constants import ControlType, Style, StyleModifier
from pygame_gui.themes.standard import STANDARD_THEMES
from pygame_gui.themes.user import USER_THEMES

USER_THEMES_FILE = "user.py"

main_styles = (
    Style.PRIMARY,
    Style.SECONDARY,
    Style.SUCCESS,
    Style.INFO,
    Style.WARNING,
    Style.DANGER,
)

themes: dict[str, dict[str, dict[str, Any]]] = {}
themes = STANDARD_THEMES | USER_THEMES

current_theme: str = "darkly"

style_definitiions: dict[
    ControlType, dict[StyleModifier, tuple[str, str, str, str, bool]]
] = {
    ControlType.FRAME: {
        StyleModifier.DEFAULT: (
            "STYLE",
            "foreground",
            "foreground",
            "foreground",
            False,
        ),
        StyleModifier.OUTLINE: ("NONE", "STYLE", "NONE", "STYLE", False),
    },
    ControlType.LABEL: {
        StyleModifier.DEFAULT: ("NONE", "NONE", "NONE", "STYLE", False),
        StyleModifier.OUTLINE: ("NONE", "STYLE", "NONE", "STYLE", False),
        StyleModifier.INVERSE: ("STYLE", "STYLE", "NONE", "foreground", False),
    },
    ControlType.TEXTBLOCK: {
        StyleModifier.DEFAULT: ("NONE", "NONE", "NONE", "STYLE", False),
        StyleModifier.OUTLINE: ("NONE", "STYLE", "NONE", "STYLE", False),
        StyleModifier.INVERSE: ("STYLE", "STYLE", "NONE", "foreground", False),
    },
    ControlType.BUTTON: {
        StyleModifier.DEFAULT: ("STYLE", "STYLE", "foreground", "foreground", True),
        StyleModifier.OUTLINE: ("NONE", "STYLE", "STYLE", "STYLE", True),
        StyleModifier.SIMPLE: ("NONE", "NONE", "STYLE", "STYLE", True),
    },
    ControlType.TOGGLEBUTTON: {
        StyleModifier.DEFAULT: ("STYLE", "STYLE", "foreground", "foreground", True),
        StyleModifier.OUTLINE: ("NONE", "STYLE", "STYLE", "STYLE", True),
        StyleModifier.SIMPLE: ("NONE", "NONE", "STYLE", "STYLE", True),
    },
    ControlType.TOGGLESWITCH: {
        StyleModifier.DEFAULT: ("NONE", "NONE", "NONE", "STYLE", False),
    },
    ControlType.TOGGLESWITCHROUNDEL: {
        StyleModifier.DEFAULT: ("STYLE", "STYLE", "foreground", "STYLE", True),
    },
    ControlType.RADIOBUTTON: {
        StyleModifier.DEFAULT: ("STYLE", "STYLE", "foreground", "foreground", True),
        StyleModifier.OUTLINE: ("NONE", "STYLE", "STYLE", "STYLE", True),
        StyleModifier.SIMPLE: ("NONE", "NONE", "STYLE", "STYLE", True),
    },
    ControlType.RADIOSWITCH: {
        StyleModifier.DEFAULT: ("NONE", "NONE", "NONE", "STYLE", False),
    },
    ControlType.RADIOSWITCHROUNDEL: {
        StyleModifier.DEFAULT: ("STYLE", "STYLE", "foreground", "STYLE", True),
    },
    ControlType.LISTBOX: {
        StyleModifier.DEFAULT: ("STYLE", "STYLE", "STYLE", "foreground", False),
        StyleModifier.OUTLINE: ("NONE", "STYLE", "NONE", "STYLE", False),
    },
    ControlType.LISTBOXITEM: {
        StyleModifier.DEFAULT: ("STYLE", "STYLE", "STYLE", "foreground", True),
        StyleModifier.OUTLINE: ("NONE", "NONE", "NONE", "STYLE", True),
    },
    ControlType.ENTRYBOX: {
        StyleModifier.DEFAULT: ("STYLE", "STYLE", "NONE", "foreground", True),
        StyleModifier.OUTLINE: ("NONE", "STYLE", "NONE", "STYLE", True),
    },
    ControlType.PANEL: {
        StyleModifier.DEFAULT: (
            "STYLE",
            "foreground",
            "foreground",
            "foreground",
            False,
        ),
    },
    ControlType.MESSAGEBOX: {
        StyleModifier.DEFAULT: ("default", "STYLE", "NONE", "foreground", False),
    },
    ControlType.COLORPICKER: {
        StyleModifier.DEFAULT: ("default", "STYLE", "NONE", "foreground", False),
    },
    ControlType.PROGRESSBAR: {
        StyleModifier.DEFAULT: ("NONE", "STYLE", "STYLE", "foreground", False),
        StyleModifier.INVERSE: ("NONE", "STYLE", "foreground", "STYLE", False),
    },
    ControlType.ROUNDEL: {
        StyleModifier.DEFAULT: ("STYLE", "STYLE", "foreground", "NONE", True),
        StyleModifier.OUTLINE: ("NONE", "STYLE", "STYLE", "NONE", False),
        StyleModifier.INVERSE: ("foreground", "foreground", "STYLE", "NONE", False),
    },
    ControlType.SLIDER: {
        StyleModifier.DEFAULT: ("NONE", "NONE", "foreground", "STYLE", False),
        StyleModifier.OUTLINE: ("NONE", "STYLE", "foreground", "STYLE", False),
        StyleModifier.INVERSE: ("STYLE", "STYLE", "STYLE", "foreground", False),
    },
    ControlType.MENUBUTTON: {
        StyleModifier.DEFAULT: ("STYLE", "STYLE", "foreground", "foreground", True),
        StyleModifier.OUTLINE: ("NONE", "STYLE", "STYLE", "STYLE", True),
        StyleModifier.SIMPLE: ("NONE", "NONE", "STYLE", "STYLE", True),
    },
    ControlType.MENU: {
        StyleModifier.DEFAULT: (
            "STYLE",
            "STYLE",
            "foreground",
            "foreground",
            False,
        ),
    },
}

# Theme functions.
#   - set_theme
#   - rename_theme
#   - new_theme
#   - write_themes
#   - colors_for
#   - colors_for_style
#   - lookup_color_for_style
#   - check_valid_styles
#   - lighten_hex


def set_theme(theme: str) -> None:
    """Sets the current theme."""

    # I know - but just this once!
    global current_theme  # pylint: disable=global-statement
    current_theme = theme


def rename_theme(old_theme_name: str, new_theme_name: str) -> None:
    """Renames a theme. Actually it creates a duplicate theme
    with the new name then deletes the theme with the old name."""

    if old_theme_name in USER_THEMES:

        # Create new theme and delete the old one.
        # This is the version in memory.

        themes[new_theme_name] = themes[old_theme_name]
        del themes[old_theme_name]

        # Create new theme and delete the old one.
        # This is the version to write to disk.

        USER_THEMES[new_theme_name] = USER_THEMES[old_theme_name]
        del USER_THEMES[old_theme_name]

        # Write themes to user themes file.

        write_themes()

    else:

        # It it doesn't exisit we can't rename it
        # so just create it.

        new_theme(old_theme_name, new_theme_name)


def new_theme(base_theme: str, new_theme_name: str) -> None:
    """Creates a new theme based on another theme."""

    # Create a copy of the base theme in memory.

    themes[new_theme_name] = themes[base_theme]

    # Add it to the user themes and write to file.

    USER_THEMES[new_theme_name] = themes[base_theme]

    write_themes()


def write_themes() -> None:
    """Writes themes to the user themes file."""

    # Make the path and make sure it exists.

    _output_path: Path = Path("pygame_gui", "themes") / USER_THEMES_FILE
    _output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the themes fo the user themes filre.

    with _output_path.open("w") as f:
        f.write(f"USER_THEMES={USER_THEMES}")


def colors_for(
    control_type: ControlType,
    style: Style,
    style_modifier: StyleModifier,
    active: bool,
) -> dict[str, str | None]:
    """Gets the colours for the control type for the given style and state."""

    # Raise an error if the control type does not have a valid style
    # or style_modifer registered.

    check_valid_styles(control_type, style, style_modifier)

    # Get the appropriate colors, based of style and style_modifier.

    _background: str | None = None
    _border: str | None = None
    _selection: str | None = None
    _foreground: str | None = None

    _styles = style_definitiions[control_type][style_modifier]
    _background, _border, _selection, _foreground, _show_focuss = colors_for_style(
        style, _styles
    )

    # If the colors are for an active control (focussed or selected)
    # then create a lightened background to show active status.

    if active and _show_focuss:
        if not _background:
            _background = lookup_color_for_style(style, "STYLE")
            _foreground = lookup_color_for_style(style, "foreground")

        if _background:
            _background = lighten_hex(_background)
        else:
            _background = None

    # Return the colors.

    return {
        "background": _background,
        "border": _border,
        "selection": _selection,
        "foreground": _foreground,
    }


def colors_for_style(
    style: Style, styles: tuple[str, str, str, str, bool]
) -> tuple[str | None, str | None, str | None, str | None, bool]:
    """Get the colors for the style."""

    # Lookup the colors for each of the styles.
    # eg. primary, secondary etc.

    _background: str | None = lookup_color_for_style(style, styles[0])
    _border: str | None = lookup_color_for_style(style, styles[1])
    _selction: str | None = lookup_color_for_style(style, styles[2])
    _foreground: str | None = lookup_color_for_style(style, styles[3])
    _show_focus: bool = styles[4]

    # Return the colors. ie. as hex color codes.

    return _background, _border, _selction, _foreground, _show_focus


def lookup_color_for_style(style: Style, element: str) -> str | None:
    """Looks up the color of the given element."""

    # Deal with special cases.

    if element == "NONE":
        return None

    if element == "STYLE":
        element = style.value

    # Loo up color in themes in memory.

    return themes[current_theme]["colors"][element]


def check_valid_styles(
    control_type: ControlType, style: Style, style_modifier: StyleModifier
) -> None:
    """Checks that style and style modifiers are appropriate to the control type."""

    # Basic checks.

    if control_type not in ControlType:
        raise ValueError(
            f"Trying to retrieve colors for unrenderable / unrecognised  control: {control_type=}."
        )

    if style not in Style:
        raise ValueError(f"Trying to retrieve colors for unrecognised style: {style=}.")

    if style_modifier not in StyleModifier:
        raise ValueError(
            f"Trying to retrieve colors for unrecognised style modifier: {style_modifier=}."
        )

    if control_type not in style_definitiions:
        raise ValueError(
            f"Trying to retrieve colors for unrenderable / unrecognised  control: {control_type=}."
        )

    # Check that style and style modifiers are appropriate to the control type.

    if style_modifier not in style_definitiions[control_type]:
        raise ValueError(
            f"Invalid style modifer for control type: {style_modifier=}, {control_type=} "
        )


def lighten_hex(hex_color: str, amount: float = 0.4):
    """Lightens a hex color by a given amount (0 to 1)."""

    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)

    return f"#{r:02X}{g:02X}{b:02X}"
