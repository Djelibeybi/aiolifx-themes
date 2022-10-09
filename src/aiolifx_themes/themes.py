"""Collection of colors that can be painted onto devices."""
from __future__ import annotations

import asyncio
from functools import partial
import math
import random
from typing import AsyncGenerator, Coroutine, Iterator, NamedTuple

from aiolifx.aiolifx import Light

from .util import AwaitAioLIFX, is_multizone, single_zone, supports_extended_multizone


class Hsbk(NamedTuple):
    """Contains the hue, saturation, brightness and kelvin values for a color."""

    H: float
    S: float
    B: float
    K: int


class ThemeColor:
    """Represents a color that can be contained in a theme."""

    def __init__(
        self,
        hue: float | None,
        saturation: float | None,
        brightness: float | None,
        kelvin: int | None,
    ) -> None:
        """Initialise the theme color object."""
        self._hsbk = Hsbk(
            hue or 0,
            saturation or 0,
            brightness or 0,
            kelvin or 3500,
        )

    @property
    def hsbk(self) -> Hsbk:
        """Return the hue, saturation, brightness and kelvin values of this color."""
        return self._hsbk

    @property
    def hue(self) -> float:
        """Return the hue value for this color (range: 0-360)."""
        return self._hsbk[0]

    @property
    def saturation(self) -> float:
        """Return the saturation value for this color (range: 0-1)."""
        return self._hsbk[1]

    @property
    def brightness(self) -> float:
        """Return the brightness value for this color (range: 0-1)."""
        return self._hsbk[2]

    @property
    def kelvin(self) -> int:
        """Return the kelvin value for this color (range: 1500-9000)."""
        return self._hsbk[3]

    @classmethod
    def average(kls, colors: list[ThemeColor]) -> ThemeColor:
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

            if color.kelvin == 0:
                kelvin_total += 3500
            else:
                kelvin_total += color.kelvin

        hue = math.atan2(hue_x_total, hue_y_total) / (2.0 * math.pi)
        if hue < 0.0:
            hue += 1.0
        hue *= 360

        saturation = saturation_total / len(colors)
        brightness = brightness_total / len(colors)
        kelvin = round(kelvin_total / len(colors))

        return ThemeColor(hue, saturation, brightness, kelvin)

    def __lt__(self, other: object) -> bool:
        """A color is less than if it has lower HSBK values."""
        if not isinstance(other, ThemeColor):
            return NotImplemented
        return self.hsbk < other.hsbk

    def __gt__(self, other: object) -> bool:
        """A color is more than if it has higher HSBK values."""
        if not isinstance(other, ThemeColor):
            return NotImplemented
        return self.hsbk > other.hsbk

    def __eq__(self, other: object) -> bool:
        """Two colors are equal if they have the same HSBK values."""
        if not isinstance(other, ThemeColor):
            return NotImplemented
        return other.hsbk == self.hsbk

    def __hash__(self) -> int:
        """Returns a hash of this color has an integer."""
        return hash(self.hsbk)

    def as_dict(self) -> dict[str, float | int]:
        """Returns a dictionary of hue, saturation, brightness and kelvin."""
        return {
            "hue": self.hue,
            "saturation": self.saturation,
            "brightness": self.brightness,
            "kelvin": self.kelvin,
        }

    def as16bit(self) -> tuple[int, int, int, int]:
        """Returns a tuple of 16 bit hue, saturation, brightness and kelvin values.

        The hue, saturation and brightness values are converted to 16 bit values
        each with a range of 0-65535.
        """
        return (
            int(round(0x10000 * self.hue) / 360) % 0x10000,
            int(round(0xFFFF * self.saturation)),
            int(round(0xFFFF * self.brightness)),
            self.kelvin,
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
        return self.__class__(*self.hsbk)

    def limit_distance_to(self, other: ThemeColor) -> ThemeColor:
        """
        Return a new color with its hue within 90 degrees of this color.

        We take or add 90 depending on whether the other color is more than
        180 hue points away where that is calculated by moving forward and
        wrapping around 360.

        If the difference between the two colors is less than 90 degrees, we
        return the original color.
        """
        raw_dist = (
            self.hue - other.hue if self.hue > other.hue else other.hue - self.hue
        )
        dist = 360 - raw_dist if raw_dist > 180 else raw_dist
        if abs(dist) > 90:
            h = self.hue + 90 if (other.hue + dist) % 360 == self.hue else self.hue - 90
            if h < 0:
                h += 360
            return ThemeColor(h, self.saturation, self.brightness, self.kelvin)
        else:
            return self

    def __str__(self) -> str:
        """Return a string representation of the HSBK values for this color.."""
        h, s, b, k = self.hue, self.saturation, self.brightness, self.kelvin
        return f"H: {h}, S: {s}, B: {b}, K: {k}"


class Theme:
    """A list of colors combined to form a theme."""

    def __init__(self) -> None:
        """Initialise the theme with an empty list of colors."""
        self._colors: list[ThemeColor] = []

    @property
    def colors(self) -> list[ThemeColor]:
        """Return the a list of color dicts for this theme."""
        return [color for color in self._colors]

    def add_hsbk(
        self, hue: float, saturation: float, brightness: float, kelvin: int
    ) -> None:
        """Add a color to the list of colors."""
        self._colors.append(ThemeColor(hue, saturation, brightness, kelvin))

    def random(self) -> ThemeColor:
        """Return a random color from the list of colors."""
        return random.choice(self._colors)  # nosec

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
        new_theme._colors = colors
        return new_theme

    def ensure_color(self) -> None:
        """Ensures the theme has at least one color.."""
        if not self._colors:
            self.add_hsbk(0, 0, 1, 3500)


class ThemeLibrary:
    """Collection of predefined themes."""

    def __init__(self) -> None:
        """Initialise the library."""
        self._palettes: dict[str, list[dict[str, int | float]]] = LIFX_APP_THEMES

    @property
    def themes(self) -> list[str]:
        """Returns a list of names of the themes in the library."""
        return [name for name in self._palettes.keys()]

    def get_theme(self, theme_name: str) -> Theme:
        """Returns the named theme from the library or a blank theme."""
        theme = Theme()
        for color in self._palettes.get(theme_name, []):
            theme.add_hsbk(
                color["hue"],
                color["saturation"],
                color["brightness"],
                int(color["kelvin"]),
            )
        theme.ensure_color()
        return theme

    def get_theme_colors(self, theme_name: str) -> list[ThemeColor]:
        """Return a list of colors for the named theme or neutral white."""
        colors = self._palettes.get(theme_name, [])
        return [
            ThemeColor(
                color["hue"],
                color["saturation"],
                color["brightness"],
                int(color["kelvin"]),
            )
            for color in colors
        ]

    def get_random_theme(self) -> tuple[str, Theme]:
        """Returns a random theme from the library."""
        name = random.choice(list(self.themes))  # nosec
        theme = self.get_theme(name)
        return (name, theme)


class ThemePainter:
    """Paints themes onto LIFX devices."""

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        """Initialise the ThemePainter."""
        self._loop = loop

    async def paint_single(
        self, light: Light, color: tuple[int, int, int, int], duration: int = 0
    ) -> Coroutine:  # type: ignore
        """Paint a single color onto a normal light."""
        return await AwaitAioLIFX().wait(
            partial(light.set_color, color, duration=duration)
        )

    async def paint_multizone(
        self, light: Light, colors: list[tuple[int, int, int, int]], duration: int = 0
    ) -> Coroutine:  # type: ignore
        """Paint multiple colors onto a multizone light."""
        return await AwaitAioLIFX().wait(
            partial(
                light.set_extended_color_zones,
                colors,
                light.zones_count,
                duration=duration,
            )
        )

    async def paint_legacy_multizone(
        self, light: Light, colors: list[tuple[int, int, int, int]], duration: int = 0
    ) -> AsyncGenerator[Coroutine, None]:  # type: ignore
        """Paint each zone individually on a legacy multizone light."""
        for index, color in enumerate(colors):
            apply = 1 if (index == len(colors) - 1) else 0
            yield AwaitAioLIFX().wait(
                partial(
                    light.set_color_zones,
                    index,
                    index,
                    color,
                    apply=apply,
                    duration=int(duration),
                )
            )

    async def paint(self, theme: Theme, lights: list[Light], duration: int = 0) -> None:
        """Paint theme using a light-specific painter."""
        duration = duration * 1000

        tasks = []
        for light in lights:

            if single_zone(light):
                tasks.append(
                    self.paint_single(light, theme.random().as16bit(), duration)
                )

            elif is_multizone(light):
                """Paint a linear multizone light"""
                await AwaitAioLIFX().wait(light.get_extended_color_zones)
                colors = MultiZone().get_theme_colors(theme, light.zones_count)

                if supports_extended_multizone(light) is True:
                    # Pad to 82 zones and send a single message
                    for _ in range(len(colors), 82):
                        colors.append((0, 0, 0, 0))

                    tasks.append(self.paint_multizone(light, colors, duration))
                else:
                    # send multiple set_color_zones messages to paint the theme.
                    async for task in self.paint_legacy_multizone(
                        light, colors, duration=duration
                    ):
                        tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)


class MultiZone:
    """Generates the color values from a theme to blend onto a multizone device."""

    def __init__(self) -> None:
        """Initialise the generator with blank list of colors."""
        self._colors: list[ThemeColor] = []

    def add_color(self, color: ThemeColor) -> None:
        """Add a color to the list of colors to use."""
        self._colors.append(color)

    def apply_to_range(
        self, this_color: ThemeColor, next_color: ThemeColor, length: int
    ) -> None:
        """Recursively add two colors with a blend between them."""

        if length == 1:
            self.add_color(this_color)

        elif length == 2:
            second_color = ThemeColor.average(
                [next_color.limit_distance_to(this_color), this_color]
            )
            self.add_color(this_color)
            self.add_color(second_color)

        else:
            average = ThemeColor.average([next_color, this_color])
            self.apply_to_range(this_color, average, length // 2)
            self.apply_to_range(average, next_color, length - length // 2)

    def build_ranges(self, theme: Theme, zone_count: int) -> None:
        """Build a the list of colors in ranges based on multizone count."""
        index = 0
        location = 0
        zones_per_color = max(1, int(zone_count / max(len(theme) - 1, 1)))

        while location < zone_count:
            length = min(location + zones_per_color, zone_count) - location
            self.apply_to_range(
                theme[index], theme.get_next_bounds_checked(index), length
            )
            index = min(len(theme) - 1, index + 1)
            location += zones_per_color

    def get_theme_colors(self, theme: Theme, num_zones: int) -> list:  # type: ignore
        """Generates the list of colors for all zones to create a blended theme."""
        new_theme = theme.shuffled()
        new_theme.ensure_color()
        self.build_ranges(new_theme, num_zones)

        new_colors: list[tuple[int, int, int, int]] = []

        for (start, end), color in self.colors:
            for _ in range(0, end - start + 1):
                new_colors.append(color.as16bit())

        return new_colors

    @property
    def colors(self) -> list[tuple[tuple[int, int], ThemeColor]]:
        """Return a list of colors with start and end index values."""
        start_index = 0
        end_index = -1
        current = ThemeColor(0, 0, 0, 0)
        results: list[tuple[tuple[int, int], ThemeColor]] = []

        for color in self._colors:
            if current != color:
                result = ((start_index, end_index), current)

                results.append(result)
                start_index = end_index + 1

            end_index += 1
            current = color.clone()

        result = ((start_index, end_index), current)
        results.append(result)
        return results


LIFX_APP_THEMES = {
    "autumn": [
        {"hue": 31.0, "saturation": 1.0, "brightness": 0.5, "kelvin": 3500},
        {"hue": 83.0, "saturation": 1.0, "brightness": 0.5, "kelvin": 3500},
        {"hue": 49.0, "saturation": 1.0, "brightness": 0.5, "kelvin": 3500},
        {"hue": 58.0, "saturation": 1.0, "brightness": 0.5, "kelvin": 3500},
    ],
    "blissful": [
        {"hue": 303, "saturation": 0.18, "brightness": 0.82, "kelvin": 3500},
        {"hue": 232, "saturation": 0.46, "brightness": 0.53, "kelvin": 3500},
        {"hue": 252, "saturation": 0.37, "brightness": 0.69, "kelvin": 3500},
        {"hue": 245, "saturation": 0.29, "brightness": 0.81, "kelvin": 3500},
        {"hue": 303, "saturation": 0.37, "brightness": 0.18, "kelvin": 3500},
        {"hue": 56, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 321, "saturation": 0.39, "brightness": 0.78, "kelvin": 3500},
    ],
    "cheerful": [
        {"hue": 310, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 266, "saturation": 0.87, "brightness": 0.47, "kelvin": 3500},
        {"hue": 248, "saturation": 1.0, "brightness": 0.6, "kelvin": 3500},
        {"hue": 51, "saturation": 1.0, "brightness": 0.67, "kelvin": 3500},
        {"hue": 282, "saturation": 0.9, "brightness": 0.67, "kelvin": 3500},
    ],
    "dream": [
        {"hue": 201, "saturation": 0.76, "brightness": 0.23, "kelvin": 3500},
        {"hue": 183, "saturation": 0.75, "brightness": 0.32, "kelvin": 3500},
        {"hue": 199, "saturation": 0.22, "brightness": 0.62, "kelvin": 3500},
        {"hue": 223, "saturation": 0.22, "brightness": 0.91, "kelvin": 3500},
        {"hue": 219, "saturation": 0.29, "brightness": 0.52, "kelvin": 3500},
        {"hue": 167, "saturation": 0.62, "brightness": 0.55, "kelvin": 3500},
        {"hue": 201, "saturation": 0.76, "brightness": 0.23, "kelvin": 3500},
    ],
    "energizing": [
        {"hue": 0, "saturation": 0.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 205, "saturation": 0.47, "brightness": 1.0, "kelvin": 3500},
        {"hue": 191, "saturation": 0.89, "brightness": 1.0, "kelvin": 3500},
        {"hue": 242, "saturation": 1.0, "brightness": 0.42, "kelvin": 3500},
        {"hue": 180, "saturation": 0.87, "brightness": 0.27, "kelvin": 3500},
        {"hue": 0, "saturation": 0.0, "brightness": 0.3, "kelvin": 3500},
    ],
    "epic": [
        {"hue": 226, "saturation": 1.0, "brightness": 0.96, "kelvin": 3500},
        {"hue": 233, "saturation": 1.0, "brightness": 0.49, "kelvin": 3500},
        {"hue": 184, "saturation": 0.6, "brightness": 0.57, "kelvin": 3500},
        {"hue": 249, "saturation": 0.29, "brightness": 0.95, "kelvin": 3500},
        {"hue": 261, "saturation": 0.84, "brightness": 0.58, "kelvin": 3500},
        {"hue": 294, "saturation": 0.78, "brightness": 0.51, "kelvin": 3500},
    ],
    "exciting": [
        {"hue": 0, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 40, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 60, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 122, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 239, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 271, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 294, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
    ],
    "focusing": [
        {"hue": 338, "saturation": 0.38, "brightness": 1.0, "kelvin": 3500},
        {"hue": 42, "saturation": 0.36, "brightness": 1.0, "kelvin": 3500},
        {"hue": 52, "saturation": 0.21, "brightness": 1.0, "kelvin": 3500},
        {"hue": 0, "saturation": 0.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 0, "saturation": 0.0, "brightness": 1.0, "kelvin": 3500},
    ],
    "halloween": [
        {"hue": 31, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 32, "saturation": 1.0, "brightness": 0.6, "kelvin": 3500},
        {"hue": 32, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 33, "saturation": 1.0, "brightness": 0.6, "kelvin": 3500},
        {"hue": 33, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 34, "saturation": 1.0, "brightness": 0.7, "kelvin": 3500},
    ],
    "hanukkah": [
        {"hue": 213, "saturation": 0.52, "brightness": 1.0, "kelvin": 3500},
        {"hue": 219, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 0, "saturation": 0.0, "brightness": 0.32, "kelvin": 3500},
        {"hue": 199, "saturation": 1.0, "brightness": 0.34, "kelvin": 3500},
        {"hue": 232, "saturation": 1.0, "brightness": 0.35, "kelvin": 3500},
        {"hue": 225, "saturation": 0.25, "brightness": 0.13, "kelvin": 3500},
    ],
    "holly": [
        {"hue": 117, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 116, "saturation": 0.9, "brightness": 1.0, "kelvin": 3500},
        {"hue": 1, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 118, "saturation": 1.0, "brightness": 0.5, "kelvin": 3500},
        {"hue": 360, "saturation": 1.0, "brightness": 0.9, "kelvin": 3500},
    ],
    "independence day": [
        {"hue": 360, "saturation": 0.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 360, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 240, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
    ],
    "intense": [
        {"hue": 242, "saturation": 0.75, "brightness": 1.0, "kelvin": 3500},
        {"hue": 300, "saturation": 1.0, "brightness": 0.87, "kelvin": 3500},
        {"hue": 164, "saturation": 0.99, "brightness": 1.0, "kelvin": 3500},
        {"hue": 248, "saturation": 1.0, "brightness": 0.23, "kelvin": 3500},
    ],
    "mellow": [
        {"hue": 359, "saturation": 0.31, "brightness": 0.59, "kelvin": 3500},
        {"hue": 315, "saturation": 0.24, "brightness": 0.82, "kelvin": 3500},
        {"hue": 241, "saturation": 1.0, "brightness": 0.4, "kelvin": 3500},
        {"hue": 256, "saturation": 0.36, "brightness": 0.5, "kelvin": 3500},
        {"hue": 79, "saturation": 0.05, "brightness": 0.4, "kelvin": 3500},
    ],
    "peaceful": [
        {"hue": 198, "saturation": 0.48, "brightness": 0.11, "kelvin": 3500},
        {"hue": 2, "saturation": 0.46, "brightness": 0.85, "kelvin": 3500},
        {"hue": 54, "saturation": 0.36, "brightness": 0.85, "kelvin": 3500},
        {"hue": 4, "saturation": 0.63, "brightness": 0.56, "kelvin": 3500},
        {"hue": 203, "saturation": 0.34, "brightness": 0.56, "kelvin": 3500},
    ],
    "powerful": [
        {"hue": 10, "saturation": 0.99, "brightness": 0.66, "kelvin": 3500},
        {"hue": 59, "saturation": 0.7, "brightness": 0.98, "kelvin": 3500},
        {"hue": 11, "saturation": 0.99, "brightness": 0.41, "kelvin": 3500},
        {"hue": 61, "saturation": 0.44, "brightness": 0.99, "kelvin": 3500},
        {"hue": 18, "saturation": 0.98, "brightness": 0.98, "kelvin": 3500},
        {"hue": 52, "saturation": 0.88, "brightness": 0.97, "kelvin": 3500},
        {"hue": 52, "saturation": 0.88, "brightness": 0.97, "kelvin": 3500},
    ],
    "relaxing": [
        {"hue": 110, "saturation": 0.95, "brightness": 1.0, "kelvin": 3500},
        {"hue": 71, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 123, "saturation": 0.85, "brightness": 0.33, "kelvin": 3500},
        {"hue": 120, "saturation": 0.5, "brightness": 0.1, "kelvin": 3500},
    ],
    "santa": [
        {"hue": 0, "saturation": 1.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 351, "saturation": 0.05, "brightness": 1.0, "kelvin": 3500},
        {"hue": 2, "saturation": 1.0, "brightness": 0.58, "kelvin": 3500},
        {"hue": 0, "saturation": 0.0, "brightness": 0.52, "kelvin": 3500},
    ],
    "serene": [
        {"hue": 179, "saturation": 0.1, "brightness": 0.91, "kelvin": 3500},
        {"hue": 215, "saturation": 0.85, "brightness": 0.98, "kelvin": 3500},
        {"hue": 205, "saturation": 0.44, "brightness": 0.37, "kelvin": 3500},
        {"hue": 94, "saturation": 0.63, "brightness": 0.25, "kelvin": 3500},
        {"hue": 100, "saturation": 0.26, "brightness": 0.42, "kelvin": 3500},
        {"hue": 132, "saturation": 0.46, "brightness": 0.88, "kelvin": 3500},
        {"hue": 211, "saturation": 0.73, "brightness": 0.97, "kelvin": 3500},
    ],
    "soothing": [
        {"hue": 336, "saturation": 0.18, "brightness": 0.67, "kelvin": 3500},
        {"hue": 335, "saturation": 0.5, "brightness": 0.67, "kelvin": 3500},
        {"hue": 0, "saturation": 0.0, "brightness": 1.0, "kelvin": 3500},
        {"hue": 302, "saturation": 0.69, "brightness": 1.0, "kelvin": 3500},
        {"hue": 330, "saturation": 0.45, "brightness": 0.58, "kelvin": 3500},
    ],
    "sports": [
        {"hue": 59, "saturation": 0.81, "brightness": 0.96, "kelvin": 3500},
        {"hue": 120, "saturation": 1.0, "brightness": 0.96, "kelvin": 3500},
        {"hue": 120, "saturation": 0.74, "brightness": 1.0, "kelvin": 3500},
    ],
    "spring": [
        {"hue": 184.0, "saturation": 1.0, "brightness": 0.5, "kelvin": 3500},
        {"hue": 299.0, "saturation": 1.0, "brightness": 0.5, "kelvin": 3500},
        {"hue": 49.0, "saturation": 1.0, "brightness": 0.5, "kelvin": 3500},
        {"hue": 198.0, "saturation": 1.0, "brightness": 0.5, "kelvin": 3500},
    ],
    "tranquil": [
        {"hue": 0, "saturation": 0.0, "brightness": 0.0, "kelvin": 3500},
        {"hue": 205, "saturation": 0.74, "brightness": 0.96, "kelvin": 3500},
        {"hue": 203, "saturation": 0.94, "brightness": 0.96, "kelvin": 3500},
        {"hue": 241, "saturation": 0.99, "brightness": 1.0, "kelvin": 3500},
        {"hue": 37, "saturation": 0.75, "brightness": 0.99, "kelvin": 3500},
        {"hue": 43, "saturation": 0.83, "brightness": 0.53, "kelvin": 3500},
    ],
    "warming": [
        {"hue": 4, "saturation": 1.0, "brightness": 0.76, "kelvin": 3500},
        {"hue": 42, "saturation": 0.36, "brightness": 0.96, "kelvin": 3500},
        {"hue": 355, "saturation": 0.81, "brightness": 0.86, "kelvin": 3500},
        {"hue": 44, "saturation": 0.44, "brightness": 0.65, "kelvin": 3500},
        {"hue": 51, "saturation": 0.85, "brightness": 0.59, "kelvin": 3500},
        {"hue": 0, "saturation": 0.0, "brightness": 0.3, "kelvin": 3500},
    ],
}
