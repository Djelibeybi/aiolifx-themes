"""Utility methods for aiolifx-themes."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import cast

from aiolifx.aiolifx import Light
from aiolifx.message import Message
from aiolifx.products import features_map


def is_single(device: Light) -> bool:
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


def is_matrix(device: Light) -> bool:
    """True is device is a matrix light."""
    return bool(features_map[device.product]["matrix"] is True)


def supports_extended_multizone(device: Light) -> bool:
    """True if device is an extended multizone light."""
    return bool(features_map[device.product]["extended_multizone"] is True)


def user_coords_to_pixel_coords(
    coords_and_sizes: list[tuple[tuple[int, int], tuple[int, int]]],
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """
    Translation between user_coords_and_sizes to based on pixels.

    The user coords are what is stored on the tiles themselves
    ``[(user_x, user_y), (width, height)]``
    where user_x and user_y are the center of the tile in terms of tile
    and width and height are in terms of pixels.

    We return from this function
    ``[(user_x, user_y), (width, height)]``
    where width and height are unchanged
    and user_x and user_y are the top left of the tile in terms of pixels
    """

    user_coords: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for (x, y), (w, h) in coords_and_sizes:
        new_x = int(x * w) - int(w * 0.5)
        new_y = int(y * h) + int(h * 0.5)

        user_coords.append(((new_x, new_y), (w, h)))

    return user_coords


class AwaitAioLIFX:
    """Wait for an aiolifx callback and return the message."""

    def __init__(self) -> None:
        """Initialize the wrapper."""
        self._device: Light | None = None
        self._message: Message | None = None
        self._event = asyncio.Event()

    def callback(self, device: Light, message: Message) -> None:
        """Handle responses."""
        self._device = device
        self._message = message
        self._event.set()

    async def wait(self, method: Callable[..., None]) -> Message:
        """Call an aiolifx method and wait for its response or a timeout."""
        self._event.clear()
        method(callb=self.callback)
        await self._event.wait()
        return cast(Message, self._message)
