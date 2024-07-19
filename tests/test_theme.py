# type: ignore

from operator import contains
from unittest.mock import MagicMock

import pytest

from aiolifx_themes.library import LIFX_APP_THEMES
from aiolifx_themes.theme import Theme, ThemeColor

THEME_NAMES = [name for name in LIFX_APP_THEMES]


def test_theme_color() -> None:
    """Test the ThemeColor methods."""

    aqua = ThemeColor(180, 100, 100, 3500)
    blue = ThemeColor(240, 1.0, 1.0, 3500)
    coral = ThemeColor(16.114, 68.627, 100.0, 3500)

    rgb = MagicMock()

    assert (aqua.hue, aqua.saturation, aqua.brightness, aqua.kelvin) == (
        180,
        1,
        1,
        3500,
    )
    assert aqua < blue
    assert aqua > coral
    assert hash(aqua) == -4899733196980317225
    assert aqua.cache_key == (
        ("brightness", 1.0),
        ("hue", 180),
        ("kelvin", 3500),
        ("saturation", 1.0),
    )

    aqua_clone = aqua.clone()
    assert aqua == aqua_clone

    with pytest.raises(AssertionError):
        assert aqua == ("not", "a", "color")

    with pytest.raises(TypeError):
        assert aqua > rgb

    with pytest.raises(TypeError):
        assert aqua < rgb

    avg_kelvin = [
        ThemeColor(0, 0, 25, 2000),
        ThemeColor(0, 0, 25, 3500),
        ThemeColor(0, 0, 50, 6000),
        ThemeColor(0, 0, 75, 9000),
    ]
    kelvin_average = ThemeColor.average(avg_kelvin)
    assert kelvin_average.as_dict() == ThemeColor(0, 0, 43.75, 5125).as_dict()

    avg_colors = [
        ThemeColor(60.0, 1.0, 0.25, 3500),
        ThemeColor(120.0, 1.0, 0.5, 3500),
        ThemeColor(180.0, 1.0, 0.75, 3500),
        ThemeColor(240.0, 1.0, 1.0, 3500),
    ]
    brightness_average = ThemeColor.average(avg_colors)
    assert brightness_average.as_dict() == ThemeColor(150.0, 1.0, 0.625, 3500).as_dict()

    start_color = ThemeColor(0, 1.0, 1.0, 3500)
    end_color = ThemeColor(230, 1.0, 1.0, 3500)
    assert start_color.limit_distance_to(end_color) == ThemeColor(90, 100, 100, 3500)


def test_theme_methods() -> None:
    """Test the ThemeMethods."""

    aqua = ThemeColor(180, 100, 100, 3500)
    red = ThemeColor(0, 100, 100, 3500)

    theme = Theme()
    theme.add_hsbk(180, 100, 100, 3500)
    theme.add_hsbk(240, 100, 100, 3500)

    assert contains(theme, aqua)
    assert not contains(theme, red)

    test_colors = [
        (0, 1, 1, 3500),
        (90, 1, 1, 3500),
        (180, 1, 1, 3500),
        (270, 1, 1, 3500),
    ]
    test_theme = Theme()
    for hsbk in test_colors:
        test_theme.add_hsbk(*hsbk)
    assert len(test_theme) == 4
    assert test_theme.colors == [
        (0, 65535, 65535, 3500),
        (16384, 65535, 65535, 3500),
        (32768, 65535, 65535, 3500),
        (49152, 65535, 65535, 3500),
    ]

    blank_theme = Theme()
    blank_theme.ensure_color()
    assert len(blank_theme) == 1
    assert blank_theme.colors[0] == (0, 0, 65535, 3500)
