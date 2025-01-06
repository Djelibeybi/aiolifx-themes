"""Library of predefined themes."""

from __future__ import annotations

import logging
import random

from .theme import Theme, ThemeColor

_LOGGER = logging.getLogger(__name__)


class ThemeLibrary:
    """Collection of predefined themes."""

    def __init__(self) -> None:
        """Initialise the library."""
        self._themes: dict[str, list[ThemeColor]] = LIFX_APP_THEMES

    @property
    def themes(self) -> list[str]:
        """Returns a list of names of the themes in the library."""
        return [name for name in self._themes]

    def get_theme(self, theme_name: str) -> Theme:
        """Returns the named theme from the library or a blank theme."""
        theme = Theme()
        for color in self._themes.get(theme_name, []):
            theme.add_hsbk(color.hue, color.saturation, color.brightness, color.kelvin)
        theme.ensure_color()
        return theme

    def get_theme_colors(self, theme_name: str) -> list[ThemeColor]:
        """Return a list of colors for the named theme or neutral white."""
        return [color for color in self._themes.get(theme_name, [])]

    def get_random_theme(self) -> tuple[str, Theme]:
        """Returns a random theme from the library."""
        name = random.choice(list(self.themes))
        theme = self.get_theme(name)
        return name, theme


LIFX_APP_THEMES = {
    "autumn": [
        ThemeColor(hue=31.0, saturation=1.0, brightness=0.5, kelvin=3500),
        ThemeColor(hue=83.0, saturation=1.0, brightness=0.5, kelvin=3500),
        ThemeColor(hue=49.0, saturation=1.0, brightness=0.5, kelvin=3500),
        ThemeColor(hue=58.0, saturation=1.0, brightness=0.5, kelvin=3500),
    ],
    "blissful": [
        ThemeColor(hue=303, saturation=0.18, brightness=0.82, kelvin=3500),
        ThemeColor(hue=232, saturation=0.46, brightness=0.53, kelvin=3500),
        ThemeColor(hue=252, saturation=0.37, brightness=0.69, kelvin=3500),
        ThemeColor(hue=245, saturation=0.29, brightness=0.81, kelvin=3500),
        ThemeColor(hue=303, saturation=0.37, brightness=0.18, kelvin=3500),
        ThemeColor(hue=56, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=321, saturation=0.39, brightness=0.78, kelvin=3500),
    ],
    "bias_lighting": [
        ThemeColor(hue=0, saturation=0.0, brightness=0.9019, kelvin=6500),
    ],
    "calaveras": [
        ThemeColor(hue=300.0, saturation=1.0, brightness=0.9019, kelvin=3500),
        ThemeColor(hue=270.0, saturation=1.0, brightness=0.9019, kelvin=3500),
        ThemeColor(hue=240.0, saturation=1.0, brightness=0.9019, kelvin=3500),
    ],
    "cheerful": [
        ThemeColor(hue=310, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=266, saturation=0.87, brightness=0.47, kelvin=3500),
        ThemeColor(hue=248, saturation=1.0, brightness=0.6, kelvin=3500),
        ThemeColor(hue=51, saturation=1.0, brightness=0.67, kelvin=3500),
        ThemeColor(hue=282, saturation=0.9, brightness=0.67, kelvin=3500),
    ],
    "christmas": [
        ThemeColor(hue=120.0, saturation=1.0, brightness=1.0, kelvin=6500),
        ThemeColor(hue=0.0, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=15.0, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=120.0, saturation=0.75, brightness=1.0, kelvin=3500),
    ],
    "dream": [
        ThemeColor(hue=201, saturation=0.76, brightness=0.23, kelvin=3500),
        ThemeColor(hue=183, saturation=0.75, brightness=0.32, kelvin=3500),
        ThemeColor(hue=199, saturation=0.22, brightness=0.62, kelvin=3500),
        ThemeColor(hue=223, saturation=0.22, brightness=0.91, kelvin=3500),
        ThemeColor(hue=219, saturation=0.29, brightness=0.52, kelvin=3500),
        ThemeColor(hue=167, saturation=0.62, brightness=0.55, kelvin=3500),
        ThemeColor(hue=201, saturation=0.76, brightness=0.23, kelvin=3500),
    ],
    "energizing": [
        ThemeColor(hue=0, saturation=0.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=205, saturation=0.47, brightness=1.0, kelvin=3500),
        ThemeColor(hue=191, saturation=0.89, brightness=1.0, kelvin=3500),
        ThemeColor(hue=242, saturation=1.0, brightness=0.42, kelvin=3500),
        ThemeColor(hue=180, saturation=0.87, brightness=0.27, kelvin=3500),
        ThemeColor(hue=0, saturation=0.0, brightness=0.3, kelvin=3500),
    ],
    "epic": [
        ThemeColor(hue=226, saturation=1.0, brightness=0.96, kelvin=3500),
        ThemeColor(hue=233, saturation=1.0, brightness=0.49, kelvin=3500),
        ThemeColor(hue=184, saturation=0.6, brightness=0.57, kelvin=3500),
        ThemeColor(hue=249, saturation=0.29, brightness=0.95, kelvin=3500),
        ThemeColor(hue=261, saturation=0.84, brightness=0.58, kelvin=3500),
        ThemeColor(hue=294, saturation=0.78, brightness=0.51, kelvin=3500),
    ],
    "evening": [
        ThemeColor(hue=34.0, saturation=0.75, brightness=0.902, kelvin=3500),
        ThemeColor(hue=34.0, saturation=0.8, brightness=0.902, kelvin=3500),
        ThemeColor(hue=39.0, saturation=0.75, brightness=0.902, kelvin=3500),
    ],
    "exciting": [
        ThemeColor(hue=0, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=40, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=60, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=122, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=239, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=271, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=294, saturation=1.0, brightness=1.0, kelvin=3500),
    ],
    "fantasy": [
        ThemeColor(hue=248.0, saturation=1.0, brightness=0.2074, kelvin=3500),
        ThemeColor(hue=242.0, saturation=0.75, brightness=0.902, kelvin=3500),
        ThemeColor(hue=163.99, saturation=0.99, brightness=0.902, kelvin=3500),
        ThemeColor(hue=300.0, saturation=1.0, brightness=0.7847, kelvin=3500),
    ],
    "focusing": [
        ThemeColor(hue=338, saturation=0.38, brightness=1.0, kelvin=3500),
        ThemeColor(hue=42, saturation=0.36, brightness=1.0, kelvin=3500),
        ThemeColor(hue=52, saturation=0.21, brightness=1.0, kelvin=3500),
        ThemeColor(hue=0, saturation=0.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=0, saturation=0.0, brightness=1.0, kelvin=3500),
    ],
    "gentle": [
        ThemeColor(hue=338.0, saturation=0.38, brightness=0.902, kelvin=3500),
        ThemeColor(hue=0.0, saturation=0.0, brightness=0.902, kelvin=9000),
        ThemeColor(hue=52.0, saturation=0.21, brightness=0.902, kelvin=3500),
        ThemeColor(hue=0.0, saturation=0.0, brightness=0.902, kelvin=2500),
        ThemeColor(hue=42.0, saturation=0.36, brightness=0.902, kelvin=3500),
    ],
    "halloween": [
        ThemeColor(hue=31, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=32, saturation=1.0, brightness=0.6, kelvin=3500),
        ThemeColor(hue=32, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=33, saturation=1.0, brightness=0.6, kelvin=3500),
        ThemeColor(hue=33, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=34, saturation=1.0, brightness=0.7, kelvin=3500),
    ],
    "hanukkah": [
        ThemeColor(hue=0.0, saturation=0.0, brightness=0.902, kelvin=6500),
        ThemeColor(hue=240.0, saturation=0.25, brightness=0.902, kelvin=3500),
        ThemeColor(hue=240.0, saturation=1.0, brightness=0.902, kelvin=3500),
        ThemeColor(hue=240.0, saturation=0.5, brightness=0.902, kelvin=3500),
        ThemeColor(hue=240.0, saturation=0.75, brightness=0.902, kelvin=3500),
    ],
    "holly": [
        ThemeColor(hue=117, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=116, saturation=0.9, brightness=1.0, kelvin=3500),
        ThemeColor(hue=1, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=118, saturation=1.0, brightness=0.5, kelvin=3500),
        ThemeColor(hue=360, saturation=1.0, brightness=0.9, kelvin=3500),
    ],
    "hygge": [
        ThemeColor(hue=39.0, saturation=0.75, brightness=0.9019, kelvin=3500),
        ThemeColor(hue=34.0, saturation=0.75, brightness=0.9019, kelvin=3500),
    ],
    "independence": [
        ThemeColor(hue=360, saturation=0.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=360, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=240, saturation=1.0, brightness=1.0, kelvin=3500),
    ],
    "intense": [
        ThemeColor(hue=242, saturation=0.75, brightness=1.0, kelvin=3500),
        ThemeColor(hue=300, saturation=1.0, brightness=0.87, kelvin=3500),
        ThemeColor(hue=164, saturation=0.99, brightness=1.0, kelvin=3500),
        ThemeColor(hue=248, saturation=1.0, brightness=0.23, kelvin=3500),
    ],
    "love": [
        ThemeColor(hue=315.0, saturation=0.45, brightness=0.8298, kelvin=3500),
        ThemeColor(hue=349.0, saturation=0.88, brightness=0.8117, kelvin=3500),
        ThemeColor(hue=345.0, saturation=0.76, brightness=0.9019, kelvin=3500),
        ThemeColor(hue=322.0, saturation=0.15, brightness=0.8839, kelvin=3500),
        ThemeColor(hue=307.0, saturation=0.16, brightness=0.9019, kelvin=3500),
    ],
    "kwanzaa": [
        ThemeColor(hue=120.0, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=0.0, saturation=1.0, brightness=1.0, kelvin=3500),
    ],
    "mellow": [
        ThemeColor(hue=359, saturation=0.31, brightness=0.59, kelvin=3500),
        ThemeColor(hue=315, saturation=0.24, brightness=0.82, kelvin=3500),
        ThemeColor(hue=241, saturation=1.0, brightness=0.4, kelvin=3500),
        ThemeColor(hue=256, saturation=0.36, brightness=0.5, kelvin=3500),
        ThemeColor(hue=79, saturation=0.05, brightness=0.4, kelvin=3500),
    ],
    "party": [
        ThemeColor(hue=300.0, saturation=1.0, brightness=0.902, kelvin=3500),
        ThemeColor(hue=265.0, saturation=1.0, brightness=0.902, kelvin=3500),
        ThemeColor(hue=240.0, saturation=1.0, brightness=0.902, kelvin=3500),
        ThemeColor(hue=240.0, saturation=0.75, brightness=0.902, kelvin=3500),
        ThemeColor(hue=214.0, saturation=0.85, brightness=0.902, kelvin=3500),
    ],
    "peaceful": [
        ThemeColor(hue=198, saturation=0.48, brightness=0.11, kelvin=3500),
        ThemeColor(hue=2, saturation=0.46, brightness=0.85, kelvin=3500),
        ThemeColor(hue=54, saturation=0.36, brightness=0.85, kelvin=3500),
        ThemeColor(hue=4, saturation=0.63, brightness=0.56, kelvin=3500),
        ThemeColor(hue=203, saturation=0.34, brightness=0.56, kelvin=3500),
    ],
    "powerful": [
        ThemeColor(hue=10, saturation=0.99, brightness=0.66, kelvin=3500),
        ThemeColor(hue=59, saturation=0.7, brightness=0.98, kelvin=3500),
        ThemeColor(hue=11, saturation=0.99, brightness=0.41, kelvin=3500),
        ThemeColor(hue=61, saturation=0.44, brightness=0.99, kelvin=3500),
        ThemeColor(hue=18, saturation=0.98, brightness=0.98, kelvin=3500),
        ThemeColor(hue=52, saturation=0.88, brightness=0.97, kelvin=3500),
        ThemeColor(hue=52, saturation=0.88, brightness=0.97, kelvin=3500),
    ],
    "proud": [
        ThemeColor(hue=32.0, saturation=1.0, brightness=0.9019, kelvin=3500),
        ThemeColor(hue=271.0, saturation=1.0, brightness=0.9019, kelvin=3500),
        ThemeColor(hue=349.0, saturation=0.88, brightness=0.8117, kelvin=3500),
        ThemeColor(hue=215.0, saturation=0.85, brightness=0.8839, kelvin=3500),
        ThemeColor(hue=120.0, saturation=0.5, brightness=0.8117, kelvin=3500),
        ThemeColor(hue=303.0, saturation=0.2, brightness=0.9019, kelvin=3500),
        ThemeColor(hue=60.0, saturation=1.0, brightness=0.9019, kelvin=3500),
    ],
    "pumpkin": [
        ThemeColor(hue=40.0, saturation=1.0, brightness=0.8532, kelvin=3500),
        ThemeColor(hue=10.0, saturation=1.0, brightness=0.4388, kelvin=3500),
        ThemeColor(hue=33.0, saturation=1.0, brightness=0.4875, kelvin=3500),
        ThemeColor(hue=45.99, saturation=1.0, brightness=0.8532, kelvin=3500),
        ThemeColor(hue=45.99, saturation=1.0, brightness=0.8532, kelvin=3500),
        ThemeColor(hue=40.0, saturation=0.55, brightness=0.9019, kelvin=3500),
    ],
    "relaxing": [
        ThemeColor(hue=110, saturation=0.95, brightness=1.0, kelvin=3500),
        ThemeColor(hue=71, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=123, saturation=0.85, brightness=0.33, kelvin=3500),
        ThemeColor(hue=120, saturation=0.5, brightness=0.1, kelvin=3500),
    ],
    "romance": [
        ThemeColor(hue=315.0, saturation=0.45, brightness=0.8298, kelvin=3500),
        ThemeColor(hue=349.0, saturation=0.88, brightness=0.8117, kelvin=3500),
        ThemeColor(hue=345.0, saturation=0.76, brightness=0.9019, kelvin=3500),
        ThemeColor(hue=322.0, saturation=0.15, brightness=0.8839, kelvin=3500),
        ThemeColor(hue=307.0, saturation=0.16, brightness=0.9019, kelvin=3500),
    ],
    "santa": [
        ThemeColor(hue=0, saturation=1.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=351, saturation=0.05, brightness=1.0, kelvin=3500),
        ThemeColor(hue=2, saturation=1.0, brightness=0.58, kelvin=3500),
        ThemeColor(hue=0, saturation=0.0, brightness=0.52, kelvin=3500),
    ],
    "serene": [
        ThemeColor(hue=179, saturation=0.1, brightness=0.91, kelvin=3500),
        ThemeColor(hue=215, saturation=0.85, brightness=0.98, kelvin=3500),
        ThemeColor(hue=205, saturation=0.44, brightness=0.37, kelvin=3500),
        ThemeColor(hue=94, saturation=0.63, brightness=0.25, kelvin=3500),
        ThemeColor(hue=100, saturation=0.26, brightness=0.42, kelvin=3500),
        ThemeColor(hue=132, saturation=0.46, brightness=0.88, kelvin=3500),
        ThemeColor(hue=211, saturation=0.73, brightness=0.97, kelvin=3500),
    ],
    "shamrock": [
        ThemeColor(hue=125.0, saturation=1.0, brightness=0.9019, kelvin=3500),
        ThemeColor(hue=130.0, saturation=0.85, brightness=0.6764, kelvin=3500),
        ThemeColor(hue=100.0, saturation=1.0, brightness=0.8117, kelvin=3500),
        ThemeColor(hue=135.0, saturation=0.5, brightness=0.4509, kelvin=3500),
        ThemeColor(hue=110.0, saturation=1.0, brightness=0.7666, kelvin=3500),
        ThemeColor(hue=120.0, saturation=1.0, brightness=0.9019, kelvin=3500),
    ],
    "soothing": [
        ThemeColor(hue=336, saturation=0.18, brightness=0.67, kelvin=3500),
        ThemeColor(hue=335, saturation=0.5, brightness=0.67, kelvin=3500),
        ThemeColor(hue=0, saturation=0.0, brightness=1.0, kelvin=3500),
        ThemeColor(hue=302, saturation=0.69, brightness=1.0, kelvin=3500),
        ThemeColor(hue=330, saturation=0.45, brightness=0.58, kelvin=3500),
    ],
    "spacey": [
        ThemeColor(hue=120.0, saturation=0.5, brightness=0.0902, kelvin=3500),
        ThemeColor(hue=70.99, saturation=1.0, brightness=0.902, kelvin=3500),
        ThemeColor(hue=110.0, saturation=0.95, brightness=0.902, kelvin=3500),
        ThemeColor(hue=123.0, saturation=0.85, brightness=0.2976, kelvin=3500),
    ],
    "sports": [
        ThemeColor(hue=59, saturation=0.81, brightness=0.96, kelvin=3500),
        ThemeColor(hue=120, saturation=1.0, brightness=0.96, kelvin=3500),
        ThemeColor(hue=120, saturation=0.74, brightness=1.0, kelvin=3500),
    ],
    "spring": [
        ThemeColor(hue=184.0, saturation=1.0, brightness=0.5, kelvin=3500),
        ThemeColor(hue=299.0, saturation=1.0, brightness=0.5, kelvin=3500),
        ThemeColor(hue=49.0, saturation=1.0, brightness=0.5, kelvin=3500),
        ThemeColor(hue=198.0, saturation=1.0, brightness=0.5, kelvin=3500),
    ],
    "stardust": [
        ThemeColor(hue=0.0, saturation=0.0, brightness=0.902, kelvin=6500),
        ThemeColor(hue=209.0, saturation=0.5, brightness=0.902, kelvin=3500),
        ThemeColor(hue=0.0, saturation=0.0, brightness=0.902, kelvin=6497),
        ThemeColor(hue=260.0, saturation=0.3, brightness=0.902, kelvin=3500),
    ],
    "thanksgiving": [
        ThemeColor(hue=50.0, saturation=0.81, brightness=0.7757, kelvin=3500),
        ThemeColor(hue=35.0, saturation=0.81, brightness=0.7757, kelvin=3500),
        ThemeColor(hue=30.0, saturation=1.0, brightness=0.902, kelvin=3500),
        ThemeColor(hue=35.0, saturation=0.85, brightness=0.5863, kelvin=3500),
        ThemeColor(hue=15.0, saturation=0.44, brightness=0.5863, kelvin=3500),
    ],
    "tranquil": [
        ThemeColor(hue=0, saturation=0.0, brightness=0.0, kelvin=3500),
        ThemeColor(hue=205, saturation=0.74, brightness=0.96, kelvin=3500),
        ThemeColor(hue=203, saturation=0.94, brightness=0.96, kelvin=3500),
        ThemeColor(hue=241, saturation=0.99, brightness=1.0, kelvin=3500),
        ThemeColor(hue=37, saturation=0.75, brightness=0.99, kelvin=3500),
        ThemeColor(hue=43, saturation=0.83, brightness=0.53, kelvin=3500),
    ],
    "warming": [
        ThemeColor(hue=4, saturation=1.0, brightness=0.76, kelvin=3500),
        ThemeColor(hue=42, saturation=0.36, brightness=0.96, kelvin=3500),
        ThemeColor(hue=355, saturation=0.81, brightness=0.86, kelvin=3500),
        ThemeColor(hue=44, saturation=0.44, brightness=0.65, kelvin=3500),
        ThemeColor(hue=51, saturation=0.85, brightness=0.59, kelvin=3500),
        ThemeColor(hue=0, saturation=0.0, brightness=0.3, kelvin=3500),
    ],
    "zombie": [
        ThemeColor(hue=155.99, saturation=1.0, brightness=0.9019, kelvin=3500),
        ThemeColor(hue=155.99, saturation=1.0, brightness=0.9019, kelvin=3500),
        ThemeColor(hue=270.0, saturation=1.0, brightness=0.859, kelvin=3500),
        ThemeColor(hue=147.0, saturation=1.0, brightness=0.4295, kelvin=3500),
        ThemeColor(hue=281.0, saturation=1.0, brightness=0.4295, kelvin=3500),
        ThemeColor(hue=138.99, saturation=1.0, brightness=0.6442, kelvin=3500),
    ],
}
