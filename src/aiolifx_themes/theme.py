"""Collection of colors that can be painted onto devices."""

from __future__ import annotations

import math
import random
from collections.abc import Iterator


class ThemeColor:
    """Represents a color that can be contained in a theme."""

    def __init__(
        self,
        hue: float = 0,
        saturation: float = 0,
        brightness: float = 0,
        kelvin: int = 3500,
    ) -> None:
        """Initialise the theme color object."""
        self.hue = hue
        self.saturation = saturation if saturation <= 1 else saturation / 100
        self.brightness = brightness if brightness <= 1 else brightness / 100
        self.kelvin = kelvin

    @classmethod
    def average(cls, colors: list[ThemeColor]) -> ThemeColor:
        """Return the average of all provided colors as a new color."""

        hue_x_total = 0.0
        hue_y_total = 0.0
        saturation_total = 0.0
        brightness_total = 0.0
        kelvin_total = 0.0

        for color in colors:
            hue_x_total += math.sin(color.hue * 2.0 * math.pi / 360)
            hue_y_total += math.cos(color.hue * 2.0 * math.pi / 360)
            saturation_total += color.saturation
            brightness_total += color.brightness
            kelvin_total += color.kelvin

        hue = math.atan2(hue_x_total, hue_y_total) / (2.0 * math.pi)
        if hue < 0.0:
            hue += 1.0
        hue *= 360
        hue = round(hue, 4)
        saturation = round(saturation_total / len(colors), 4)
        brightness = round(brightness_total / len(colors), 4)
        kelvin = round(kelvin_total / len(colors))

        return ThemeColor(hue, saturation, brightness, kelvin)

    def __lt__(self, other: object) -> bool:
        """A color is less than another color if it has lower HSBK values."""
        if not isinstance(other, ThemeColor):
            return NotImplemented

        return (self.hue, self.saturation, self.brightness, self.kelvin) < (
            other.hue,
            other.saturation,
            other.brightness,
            other.kelvin,
        )

    def __gt__(self, other: object) -> bool:
        """A color is more than another color if it has higher HSBK values."""
        if not isinstance(other, ThemeColor):
            return NotImplemented

        return (self.hue, self.saturation, self.brightness, self.kelvin) > (
            other.hue,
            other.saturation,
            other.brightness,
            other.kelvin,
        )

    def __eq__(self, other: object) -> bool:
        """Two colors are equal if they have the same HSBK values."""
        if not isinstance(other, ThemeColor):
            return NotImplemented
        return (
            other.hue == self.hue
            and other.saturation == self.saturation
            and other.brightness == self.brightness
            and other.kelvin == self.kelvin
        )

    def __hash__(self) -> int:
        """Returns a hash of this color as an integer."""
        return hash((self.hue, self.saturation, self.brightness, self.kelvin))

    def as_dict(self) -> dict[str, float | int]:
        """Returns a dictionary of hue, saturation, brightness and kelvin."""
        return {
            "hue": self.hue,
            "saturation": self.saturation,
            "brightness": self.brightness,
            "kelvin": self.kelvin,
        }

    def as_tuple(self) -> tuple[int, int, int, int]:
        """Returns a tuple of 16 bit hue, saturation, brightness and kelvin values.

        The hue, saturation and brightness values are converted to 16 bit values
        each with a range of 0-65535.
        """
        return (
            int(round(0x10000 * self.hue) / 360) % 0x10000,
            int(round(0xFFFF * self.saturation)),
            int(round(0xFFFF * self.brightness)),
            int(self.kelvin),
        )

    @property
    def cache_key(
        self,
    ) -> tuple[
        tuple[str, float], tuple[str, float], tuple[str, int], tuple[str, float]
    ]:
        """Returns a tuple of tuples for hue, saturation, brightness and kelvin."""
        return (
            ("brightness", self.brightness),
            ("hue", self.hue),
            ("kelvin", self.kelvin),
            ("saturation", self.saturation),
        )

    def clone(self) -> ThemeColor:
        """Return another color with the same HSBK values."""
        hsbk = self.as_dict()
        return ThemeColor(
            hsbk["hue"], hsbk["saturation"], hsbk["brightness"], int(hsbk["kelvin"])
        )

    def limit_distance_to(self, other: ThemeColor) -> ThemeColor:
        """
        Return a new color with its hue within 90 degrees of this color.

        This adds or subtracts 90 degrees from the hue value based on whether
        the other color is more or less than 180 degrees from this one.

        If the difference between the two colors is less than 90 degrees, we
        return the original color.
        """
        raw_dist = (
            self.hue - other.hue if self.hue > other.hue else other.hue - self.hue
        )
        dist = 360 - raw_dist if raw_dist > 180 else raw_dist
        if abs(dist) > 90:
            h = self.hue + 90 if (other.hue + dist) % 360 == self.hue else self.hue - 90
            h = h + 360 if h < 0 else h
            return ThemeColor(h, self.saturation, self.brightness, self.kelvin)
        else:
            return self

    def __str__(self) -> str:
        """Return a string representation of the HSBK values for this color."""
        string = "H: {:.0f}, S: {:.4f}, B: {:.4f}, K: {}".format(
            self.hue, self.saturation, self.brightness, self.kelvin
        )
        return string

    def __repr__(self) -> str:
        """Return a string representation of the HSBK values for this color."""
        repr = "<ThemeColor ({:.0f}, {:.4f}, {:.4f}, {})>".format(
            self.hue, self.saturation, self.brightness, self.kelvin
        )
        return repr


class Theme:
    """A list of colors combined to form a theme."""

    def __init__(self) -> None:
        """Initialise the theme with an empty list of colors."""
        self._colors: list[ThemeColor] = []

    @property
    def colors(self) -> list[tuple[int, int, int, int]]:
        """Return the list of color dicts for this theme."""
        return [color.as_tuple() for color in self._colors]

    def add_hsbk(
        self, hue: float, saturation: float, brightness: float, kelvin: int
    ) -> None:
        """Add a color to the list of colors."""
        self._colors.append(ThemeColor(hue, saturation, brightness, kelvin))

    def random(self) -> ThemeColor:
        """Return a random color from the list of colors."""
        return random.choice(self._colors)

    def __len__(self) -> int:
        """Return the number of colors in this theme."""
        return len(self._colors)

    def __iter__(self) -> Iterator[ThemeColor]:
        """Iterate over the colors in this theme."""
        return iter(self._colors)

    def __contains__(self, color: object) -> bool:
        """True if the specified color is contained in this theme."""
        return any(c == color for c in self)

    def __getitem__(self, index: int) -> ThemeColor:
        """Return the color at the index specified in this theme."""
        return self._colors[index]

    def get_next_bounds_checked(self, index: int) -> ThemeColor:
        """Return the next color after index or the last color."""
        return self[index + 1] if index + 1 < len(self) else self[index]

    def shuffled(self) -> Theme:
        """Return a new theme with the same colors as this theme but shuffled."""
        new_theme = Theme()
        colors = list(self._colors)
        random.shuffle(colors)
        for color in colors:
            new_theme.add_hsbk(
                hue=color.hue,
                saturation=color.saturation,
                brightness=color.brightness,
                kelvin=color.kelvin,
            )
        return new_theme

    def ensure_color(self) -> None:
        """Ensures the theme has at least one color."""
        if not self._colors:
            self.add_hsbk(0, 0, 1, 3500)
