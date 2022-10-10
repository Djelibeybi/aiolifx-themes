"""Tests for all ThemeColor methods."""
from __future__ import annotations

import asyncio
from operator import contains
import random
from unittest.mock import MagicMock

import pytest

from aiolifx_themes.themes import (
    LIFX_APP_THEMES,
    Theme,
    ThemeColor,
    ThemeLibrary,
    ThemePainter,
)

from . import _mocked_beam, _mocked_light, _mocked_z_strip  # type: ignore

THEME_NAMES = [name for name in LIFX_APP_THEMES.keys()]


def test_theme_color() -> None:
    """Test the ThemeColor methods."""

    aqua = ThemeColor(180, 100, 100, 3500)
    blue = ThemeColor(240, 1.0, 1.0, 3500)
    coral = ThemeColor(16.114, 68.627, 100.0, 3500)

    rgb = MagicMock()

    assert aqua.hsbk == (180, 1, 1, 3500)
    assert aqua < blue
    assert aqua > coral
    assert hash(aqua) == -4899733196980317225
    assert aqua.cache_key == (
        ("brightness", 1.0),
        ("hue", 180),
        ("kelvin", 3500),
        ("saturation", 1.0),
    )

    assert aqua == aqua.clone()

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
        ThemeColor(60.0, 1.0, 0.25, 0),
        ThemeColor(120.0, 1.0, 0.5, 0),
        ThemeColor(180.0, 1.0, 0.75, 0),
        ThemeColor(240.0, 1.0, 1.0, 0),
    ]
    brightness_average = ThemeColor.average(avg_colors)
    assert brightness_average.as_dict() == ThemeColor(150.0, 1.0, 0.625, 3500).as_dict()

    start_color = ThemeColor(0, 1.0, 1.0, 3500)
    end_color = ThemeColor(230, 1.0, 1.0, 3500)
    assert start_color.limit_distance_to(end_color) == ThemeColor(90, 100, 100, 3500)


def test_theme() -> None:
    """Test the ThemeMethods."""

    aqua = ThemeColor(180, 100, 100, 3500)
    red = ThemeColor(0, 100, 100, 3500)

    theme = Theme()
    theme.add_hsbk(180, 100, 100, 3500)
    theme.add_hsbk(240, 100, 100, 3500)

    assert contains(theme, aqua)
    assert not contains(theme, red)

    test_colors = [
        (0, 1, 1, 0),
        (90, 1, 1, 0),
        (180, 1, 1, 0),
        (270, 1, 1, 0),
    ]
    test_theme = Theme()
    for hsbk in test_colors:
        test_theme.add_hsbk(*hsbk)
    assert len(test_theme) == 4
    assert test_theme.colors == [
        (0, 65535, 65535, 0),
        (16384, 65535, 65535, 0),
        (32768, 65535, 65535, 0),
        (49152, 65535, 65535, 0),
    ]

    blank_theme = Theme()
    blank_theme.ensure_color()
    assert len(blank_theme) == 1
    assert blank_theme.colors[0] == (0, 0, 65535, 3500)


def test_theme_library() -> None:
    """Test the theme librarian."""
    library = ThemeLibrary()
    themes = library.themes
    assert len(themes) == 24

    for theme_name in ["exciting", "intense", "autumn"]:
        theme_colors = library.get_theme_colors(theme_name)
        assert [color.as_dict() for color in theme_colors] == LIFX_APP_THEMES[
            theme_name
        ]

    random_name, random_theme = library.get_random_theme()
    random_theme_colors = random_theme.colors
    color_names = [str(color) for color in random_theme]
    assert len(color_names) == len(random_theme)
    assert len(random_theme_colors) == len(color_names)

    lifx_colors = [
        ThemeColor(
            color["hue"], color["saturation"], color["brightness"], int(color["kelvin"])
        )
        for color in LIFX_APP_THEMES[random_name]
    ]
    single_color = random.choice(lifx_colors)
    assert isinstance(single_color, ThemeColor)
    assert contains(random_theme, single_color)


@pytest.mark.asyncio
async def test_theme_painter() -> None:
    """Test the theme painter."""
    lights = [_mocked_light(), _mocked_z_strip(), _mocked_beam()]
    library = ThemeLibrary()

    theme = library.get_theme("dream")
    painter = ThemePainter(asyncio.get_event_loop_policy().get_event_loop())
    await painter.paint(theme, lights)

    for light in lights:

        if light.product == 38:
            assert len(light.set_extended_color_zones.calls) == 1
        elif light.product == 31:
            assert len(light.set_color_zones.calls) == light.zones_count
        elif light.product == 22:
            assert len(light.set_color.calls) == 1
