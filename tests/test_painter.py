# type: ignore

import pytest

from aiolifx_themes.themes import ThemeLibrary, ThemePainter

from . import _mocked_beam, _mocked_light, _mocked_tile, _mocked_z_strip


@pytest.mark.asyncio
async def test_theme_painter() -> None:
    """Test the theme painter."""
    lights = [_mocked_light(), _mocked_z_strip(), _mocked_beam(), _mocked_tile()]
    library = ThemeLibrary()
    theme = library.get_theme("dream")

    await ThemePainter().paint(theme, lights, duration=0.25)

    for light in lights:
        if light.product == 38:
            # only send a single set_extended_color_zone packet
            assert len(light.set_extended_color_zones.calls) == 1
        elif light.product == 31:
            # send a packet for each zone
            assert len(light.set_color_zones.calls) == light.zones_count
            # packets in the sequence accumulate
            assert (
                light.set_color_zones.calls[round(light.zones_count / 2)][1]["apply"]
                == 0
            )
            # the last packet triggers the change
            assert light.set_color_zones.calls[light.zones_count - 1][1]["apply"] == 1
        elif light.product == 22:
            # single zone bulbs get one packet too
            assert len(light.set_color.calls) == 1
        elif light.product == 55:
            assert len(light.set64.calls) == 5
