"""Single light theme applier."""

from __future__ import annotations

from ..theme import Theme


class SingleGenerator:
    """Get a random color from the theme to apply it to a single zone device."""

    def __init__(self, theme: Theme) -> None:
        """Initialize the applier."""
        self.theme = theme

    def get_theme_color(self) -> dict[str, int]:
        """Apply a color from the theme to the light."""
        theme = self.theme.shuffled()
        theme.ensure_color()
        color = theme.random().as_tuple()
        return {
            "hue": color[0],
            "saturation": color[1],
            "brightness": color[2],
            "kelvin": color[3],
        }
