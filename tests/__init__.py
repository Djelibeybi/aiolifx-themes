# type: ignore

import asyncio
import random
from typing import Any
from unittest.mock import AsyncMock

from aiolifx.aiolifx import Light


def random_mac_addr() -> str:
    return ":".join(
        str(f"{random.getrandbits(48):x}")[i : i + 2]  # noqa: E203
        for i in range(0, 12, 2)
    )


def random_ip_addr() -> str:
    return f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"


class MockMessage:
    """Mock a lifx message."""

    def __init__(self, serial: str, **kwargs: dict[str, Any]):
        """Init message."""
        self.target_addr = serial
        self.count = 9
        for k, v in kwargs.items():
            if k != "callb":
                setattr(self, k, v)


class MockFailingLifxCommand:
    """Mock a lifx command that fails."""

    def __init__(self, bulb: Light) -> None:
        """Init command."""
        self.bulb = bulb
        self.calls: list[Any] = []

    def __call__(self, *args, **kwargs) -> None:
        """Call command."""
        if callb := kwargs.get("callb"):
            callb(self.bulb, None)
        self.calls.append([args, kwargs])

    def reset_mock(self) -> None:
        """Reset mock."""
        self.calls = []


class MockLifxCommand:
    """Mock a lifx command."""

    __name__ = "LIFX Command"

    def __init__(self, bulb: Light, **kwargs) -> None:
        """Init command."""
        self.bulb = bulb
        self.mac_addr = bulb.mac_addr
        self.ip_addr = bulb.ip_addr
        self.calls: list[Any] = []
        self.msg_kwargs = kwargs
        for k, v in kwargs.items():
            if k != "callb":
                setattr(self.bulb, k, v)

    def __call__(self, *args, **kwargs) -> None:
        """Call command."""
        if callb := kwargs.get("callb"):
            callb(self.bulb, MockMessage(self.bulb.mac_addr, **self.msg_kwargs))
        self.calls.append([args, kwargs])

    def reset_mock(self):
        """Reset mock."""
        self.calls = []


def _mocked_light() -> Light:
    """Mock LIFX light."""
    light = Light(asyncio.get_running_loop(), random_mac_addr(), random_ip_addr())
    light.host_firmware_version = "3.70"
    light.color = [0, 0, 1.0, 3500]
    light.power_level = 0
    light.fire_and_forget = AsyncMock()
    light.try_sending = AsyncMock()
    light.set_color = MockLifxCommand(light)
    light.get_version = MockLifxCommand(light)
    light.set_color_zones = MockLifxCommand(light)
    light.get_color_zones = MockLifxCommand(light)
    light.set_extended_color_zones = MockLifxCommand(light)
    light.get_extended_color_zones = MockLifxCommand(light)
    light.get64 = MockLifxCommand(light)
    light.set64 = MockLifxCommand(light)
    light.get_device_chain = MockLifxCommand(light)
    light.get_tile_effect = MockLifxCommand(light)
    light.label = "LIFX Color"
    light.product = 22
    light.zones_count = 1
    return light


def _mocked_z_strip() -> Light:
    """Mock legacy linear multizone light."""
    light = _mocked_light()
    light.label = "LIFX Z"
    light.product = 31
    light.zones_count = 64
    return light


def _mocked_beam() -> Light:
    """Mock extended multizone light."""
    light = _mocked_light()
    light.label = "LIFX Beam"
    light.product = 38
    light.zones_count = 71
    return light


def _mocked_tile() -> Light:
    """Mock matrix light."""
    light = _mocked_light()
    light.label = "LIFX Tile"
    light.product = 55
    light.tile_device_width = 8
    light.tile_devices = [
        {
            "accel_meas_x": 2250,
            "accel_meas_y": 35,
            "accel_meas_z": 82,
            "user_x": 0.0,
            "user_y": 1.0,
            "width": 8,
            "height": 8,
            "device_version_vendor": 1,
            "device_version_product": 55,
            "firmware_build": 1548977726000000000,
            "firmware_version_minor": 50,
            "firmware_version_major": 3,
        },
        {
            "accel_meas_x": 2085,
            "accel_meas_y": -41,
            "accel_meas_z": -1,
            "user_x": 1.0,
            "user_y": 1.0,
            "width": 8,
            "height": 8,
            "device_version_vendor": 1,
            "device_version_product": 55,
            "firmware_build": 1548977726000000000,
            "firmware_version_minor": 50,
            "firmware_version_major": 3,
        },
        {
            "accel_meas_x": 2328,
            "accel_meas_y": -20,
            "accel_meas_z": -125,
            "user_x": 2.0,
            "user_y": 1.0,
            "width": 8,
            "height": 8,
            "device_version_vendor": 1,
            "device_version_product": 55,
            "firmware_build": 1548977726000000000,
            "firmware_version_minor": 50,
            "firmware_version_major": 3,
        },
        {
            "accel_meas_x": -2198,
            "accel_meas_y": -43,
            "accel_meas_z": -116,
            "user_x": 3.0,
            "user_y": 1.0,
            "width": 8,
            "height": 8,
            "device_version_vendor": 1,
            "device_version_product": 55,
            "firmware_build": 1548977726000000000,
            "firmware_version_minor": 50,
            "firmware_version_major": 3,
        },
        {
            "accel_meas_x": 2227,
            "accel_meas_y": -67,
            "accel_meas_z": -54,
            "user_x": 4.0,
            "user_y": 1.0,
            "width": 8,
            "height": 8,
            "device_version_vendor": 1,
            "device_version_product": 55,
            "firmware_build": 1548977726000000000,
            "firmware_version_minor": 50,
            "firmware_version_major": 3,
        },
    ]

    return light
