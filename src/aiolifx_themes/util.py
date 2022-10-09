"""Utility methods for aiolifx-themes."""

from asyncio import Event
from typing import Callable, Optional

from aiolifx.aiolifx import Light
from aiolifx.message import Message
from aiolifx.products import features_map


def single_zone(device: Light) -> bool:
    """True if device is a single zone light."""
    return (
        features_map[device.product]["multizone"] is False
        and features_map[device.product]["matrix"] is False
        and features_map[device.product]["buttons"] is False
        and features_map[device.product]["relays"] is False
    )


def is_multizone(device: Light) -> bool:
    """True if device is a linear multizone light."""
    return bool(features_map[device.product]["multizone"] is True)


def supports_extended_multizone(device: Light) -> bool:
    """True if device is an extended multizone light."""
    return bool(features_map[device.product]["extended_multizone"] is True)


class AwaitAioLIFX:
    """Wait for an aiolifx callback and return the message."""

    def __init__(self) -> None:
        """Initialize the wrapper."""
        self._device: Optional[Light] = None
        self._message: Optional[Message] = None
        self._event = Event()

    def callback(self, device: Light, message: Message) -> None:
        """Handle responses."""
        self._device = device
        self._message = message
        self._event.set()

    async def wait(self, method: Callable) -> Message:  # type: ignore
        """Call an aiolifx method and wait for its response or a timeout."""
        self._event.clear()
        method(callb=self.callback)
        await self._event.wait()
        return self._message
