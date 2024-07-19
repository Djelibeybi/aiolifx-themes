# type: ignore

import random
from operator import contains

from aiolifx_themes.themes import LIFX_APP_THEMES, ThemeColor, ThemeLibrary


def test_theme_library() -> None:
    """Test the theme librarian."""
    library = ThemeLibrary()
    themes: list[str] = library.themes
    assert len(themes) == 42

    for theme_name in ["exciting", "intense", "autumn", "stardust"]:
        theme_colors = library.get_theme_colors(theme_name)
        assert [
            ThemeColor(
                hue=color.hue,
                saturation=color.saturation,
                brightness=color.brightness,
                kelvin=color.kelvin,
            )
            for color in theme_colors
        ] == LIFX_APP_THEMES[theme_name]

    random_name, random_theme = library.get_random_theme()
    random_theme_colors = random_theme.colors
    color_names = [str(color) for color in random_theme]
    assert len(color_names) == len(random_theme)
    assert len(random_theme_colors) == len(color_names)

    lifx_colors = [
        ThemeColor(color.hue, color.saturation, color.brightness, color.kelvin)
        for color in LIFX_APP_THEMES[random_name]
    ]
    single_color = random.choice(lifx_colors)
    assert isinstance(single_color, ThemeColor)
    assert contains(random_theme, single_color)
