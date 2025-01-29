"""The Canvas is a class for storing a two-dimensional grid of colors for matrix devices."""

from __future__ import annotations

import random
from collections.abc import Iterable, Iterator

from .theme import Theme, ThemeColor


def color_weighting(
    distances: list[tuple[int, ThemeColor]],
) -> Iterable[ThemeColor]:
    """Return an array of colors where there is more of a color the closer it is."""

    greatest_distance = max(dist for dist, _ in distances)

    for dist, color in distances:
        if dist == 0:
            for _ in range(int(greatest_distance)):
                yield color
        else:
            for _ in range(int(greatest_distance / dist)):
                yield color


def shuffle_point(i: int, j: int) -> tuple[int, int]:
    """Return a new (i, j) value that is the current (i, j) value plus or minus a random amount."""

    new_x = random.randint(i - 3, i + 3)
    new_y = random.randint(j - 3, j + 3)
    return new_x, new_y


def surrounding_points(i: int, j: int) -> list[tuple[int, int]]:
    """Return the points that surround the specified point."""

    return [
        (i - 1, j + 1),
        (i, j + 1),
        (i + 1, j + 1),
        (i - 1, j),
        (i + 1, j),
        (i - 1, j - 1),
        (i, j - 1),
        (i + 1, j - 1),
    ]


class Canvas:
    """
    A Canvas is a collection of points with methods for interacting with those points.

    The points are stored as (i, j) in a dictionary. The value for each point is a ThemeColor object.
    """

    def __init__(self) -> None:
        """Initialize the canvas."""
        self.points: dict[tuple[int, int], ThemeColor] = {}

    def add_points_for_tile(
        self, left_x: int, top_y: int, tile_width: int, tile_height: int, theme: Theme
    ) -> None:
        """
        Create points on the canvas around where a tile is.

        We create an area that's half the tile width/height beyond the boundary
        of the tile.

        We also spread the points out in a random manner and try to avoid having
        points next to each other.

        Multiple calls to this function will not override existing points on the
        canvas
        """
        from_x = int(left_x - tile_width * 1.5)
        to_x = int(left_x + tile_width * 1.5)
        from_y = int(top_y - tile_height * 1.5)
        to_y = int(top_y + tile_height * 1.5)

        i = from_x
        while i < to_x:
            j = from_y
            while j < to_y:
                if (i, j) not in self.points:
                    if not self.has_neighbour(i, j):
                        random_color = theme.random()
                        self[(i, j)] = random_color
                j += random.choice([i + 1 for i in range(3)])
            i += random.choice([i + 1 for i in range(3)])

    def surrounding_colors(self, i: int, j: int) -> list[ThemeColor]:
        """
        Return the colors that surround this (i, j) point.

        This will only return points that exist.
        """
        return [self[(x, y)] for x, y in surrounding_points(i, j) if (x, y) in self]

    def has_neighbour(self, i: int, j: int) -> bool:
        """Return whether there are any points around this (i, j) position"""
        return any(self.surrounding_colors(i, j))

    def shuffle_points(self) -> None:
        """
        Take all the points and move them around a random amount
        """

        new_points = {}
        for (i, j), color in self:
            new_points[shuffle_point(i, j)] = color

        self.points = new_points

    def blur(self) -> None:
        """
        For each point, find the average colour of that point plus all surrounding
        points.
        """
        new_points = {}
        for (i, j), original in self:
            colors = [original for _ in range(2)]
            for color in self.surrounding_colors(i, j):
                colors.append(color)
            new_points[(i, j)] = ThemeColor.average(colors)
        self.points = new_points

    def blur_by_distance(self) -> None:
        """
        Similar to blur but will find the 8 closest points as opposed to the 8
        surrounding points.
        """
        new_points = {}
        for (i, j), original in self:
            distances = self.closest_points(i, j, 8)
            weighted = list(color_weighting(distances))
            new_points[(i, j)] = ThemeColor.average(weighted)
        self.points = new_points

    def points_for_tile(
        self, left_x: int, top_y: int, tile_width: int, tile_height: int
    ) -> list[ThemeColor]:
        """
        Return a list of 64 hsbk values for this tile

        For any point on the tile that doesn't have a corresponding point on the
        canvas return a grey value. This is useful for when we tell the applier
        to not fill in the gaps.
        """
        result = []
        grey = ThemeColor(0, 0, 0.3, 3500)

        for j in range(top_y, top_y - tile_height, -1):
            for i in range(left_x, left_x + tile_width):
                result.append(self.get((i, j), grey))

        return result

    def fill_in_points(
        self, canvas: Canvas, left_x: int, top_y: int, tile_width: int, tile_height: int
    ) -> None:
        """
        Fill in the gaps on this canvas by blurring the points on the provided
        canvas around where our tile is.

        We blur by finding the 4 closest points for each point on our tile and
        averaging them.
        """
        for j in range(top_y, top_y - tile_height, -1):
            for i in range(left_x, left_x + tile_width):
                distances = canvas.closest_points(i, j, 4)
                weighted = list(color_weighting(distances))
                self[(i, j)] = ThemeColor.average(weighted)

    def closest_points(
        self, i: int, j: int, consider: int
    ) -> list[tuple[int, ThemeColor]]:
        """
        Return ``[(distance, color), ...]`` for the closest consider amount of points to (i, j)
        """
        distances: list[tuple[int, ThemeColor]] = []

        for (x, y), color in self:
            distances.append(((x - i) ** 2 + (y - j) ** 2, color))

        def get_key(
            dc: tuple[int, ThemeColor],
        ) -> tuple[int, tuple[float, float, float, int]]:
            return (
                dc[0],
                (dc[1].hue, dc[1].saturation, dc[1].brightness, dc[1].kelvin),
            )

        distances = sorted(distances, key=get_key)
        return distances[:consider]

    def __iter__(self) -> Iterator[tuple[tuple[int, int], ThemeColor]]:
        """Yield ``((i, j), color)`` pairs for all our points"""
        yield from self.points.items()

    def get(self, point: tuple[int, int], default_color: ThemeColor) -> ThemeColor:
        """
        Get a point or the passed in default_color value if the point doesn't exist
        """
        return self.points.get(point, default_color)

    def __getitem__(self, point: tuple[int, int]) -> ThemeColor:
        """Return the color at ``point`` where ``point`` is ``(i, j)``"""
        return self.points[point]

    def __setitem__(self, key: tuple[int, int], color: ThemeColor) -> None:
        """Set the color at ``point`` where ``point`` is ``(i, j)``"""

        self.points[key] = color

    def __contains__(self, point: tuple[int, int]) -> bool:
        """Return whether this ``point`` has a color where ``point`` is ``(i, j)``"""
        return point in self.points
