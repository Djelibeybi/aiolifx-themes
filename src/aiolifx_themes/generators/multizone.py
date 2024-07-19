"""Multizone theme applier."""

from __future__ import annotations

from ..theme import Theme, ThemeColor


class MultiZoneGenerator:
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
        """Build the list of colors in ranges based on multizone count."""
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
                new_colors.append(color.as_tuple())

        return new_colors

    @property
    def colors(self) -> list[tuple[tuple[int, int], ThemeColor]]:
        """Return a list of colors with start and end index values."""
        start_index = 0
        end_index = -1
        current = ThemeColor(0, 0, 0, 3500)
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
