"""Paint a theme onto one or more devices."""

from __future__ import annotations

import asyncio
from functools import partial

from aiolifx.aiolifx import Light

from .generators import MatrixGenerator, MultiZoneGenerator, SingleGenerator
from .theme import Theme
from .util import (
    AwaitAioLIFX,
    is_matrix,
    is_multizone,
    is_single,
    supports_extended_multizone,
)


class ThemePainter:
    """Paint a theme onto one or more single, multizone or matrix devices."""

    def __init__(self, loop: asyncio.AbstractEventLoop | None = None) -> None:
        """Initialize the theme painter."""
        self._loop = loop or asyncio.get_event_loop()

    async def paint(
        self,
        theme: Theme,
        lights: list[Light],
        duration: float = 0.25,
        power_on: bool = False,
    ) -> None:
        """Paint theme using a light-specific painter."""

        tasks = []
        for light in lights:
            if power_on:
                tasks.append(
                    AwaitAioLIFX().wait(
                        partial(
                            light.set_power, value="on", duration=int(duration * 1000)
                        )
                    )
                )

            if is_single(light):
                color = SingleGenerator(theme).get_theme_color()
                tasks.append(
                    AwaitAioLIFX().wait(
                        partial(
                            light.set_color,
                            value=color,
                            duration=int(duration * 1000),
                        )
                    )
                )

            if is_multizone(light):
                # Paint a linear multizone light
                await AwaitAioLIFX().wait(light.get_extended_color_zones)
                colors = MultiZoneGenerator().get_theme_colors(theme, light.zones_count)

                if supports_extended_multizone(light) is True:
                    tasks.append(
                        AwaitAioLIFX().wait(
                            partial(
                                light.set_extended_color_zones,
                                colors,
                                light.zones_count,
                                duration=int(duration * 1000),
                            )
                        )
                    )

                else:
                    # send multiple set_color_zones messages to paint the theme.
                    for index, color in enumerate(colors):
                        apply = 1 if (index == len(colors) - 1) else 0
                        tasks.append(
                            AwaitAioLIFX().wait(
                                partial(
                                    light.set_color_zones,
                                    index,
                                    index,
                                    color,
                                    apply=apply,
                                    duration=int(duration * 1000),
                                )
                            )
                        )

            if is_matrix(light):
                # Paint a matrix light
                await AwaitAioLIFX().wait(light.get_device_chain)
                coords_and_sizes = [
                    ((tile["user_x"], tile["user_y"]), (tile["width"], tile["height"]))
                    for tile in light.tile_devices
                ]

                generator = MatrixGenerator.from_user_coords(coords_and_sizes)

                for tile_index, theme_colors in enumerate(
                    generator.get_theme_colors(theme)
                ):
                    colors = [color.as_tuple() for color in theme_colors]

                    # set64 has no reply so no need to await it.
                    light.set64(
                        tile_index, 0, 0, 8, duration=int(duration), colors=colors
                    )

        await asyncio.gather(*tasks, return_exceptions=True)
