"""Theme applier classes."""

from __future__ import annotations

from ..canvas import Canvas

# from ..collections import TileColors
from ..theme import Theme, ThemeColor
from ..util import user_coords_to_pixel_coords


class MatrixGenerator:
    """Used to generate a random distribution of colors on a two-dimensional matrix device.

    coords_and_sizes = [((t.user_x, t.user_y), (t.width, t.height)) for t in chain]

        applier = TileApplier.from_user_coords(coords_and_sizes)

        for i, colors in enumerate(applier.apply_theme(theme)):
            # Apply colors to tile index i

    coords_and_sizes
        A list of ``((left_x, top_y), (width, height))`` representing the top
        left corner of each tile in the chain.

        Note that if you have ``((user_x, user_y), (width, height))`` values from
        asking a tile for its device chain, then use the ``from_user_coords``
        classmethod to create a TileApplier from that data.

    just_points
        Part of the algorithm generates random points on the canvas followed by
        filling in the gaps between those points. By setting this option to True
        we won't fill in the gaps

    post_blur
        By setting this to false we won't blur the points after the gaps are
        filled in.
    """

    def __init__(
        self,
        coords_and_sizes: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        """Initialize the matrix splotch applier."""
        self.coords_and_sizes: list[tuple[tuple[int, int], tuple[int, int]]] = (
            coords_and_sizes
        )

        self.tiles: list[list[ThemeColor]] = []

    @classmethod
    def from_user_coords(
        cls, coords_and_sizes: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> MatrixGenerator:
        """Create a matrix applier from the user coordinates returned by a GetDeviceChain message."""

        normalized = user_coords_to_pixel_coords(coords_and_sizes)
        return cls(normalized)

    def add_tile(self, colors: list[ThemeColor]) -> None:
        """Add a list of 64 Color objects to represent the next tile."""
        self.tiles.append(colors)

    def add_tiles_from_canvas(self, canvas: Canvas) -> None:
        """Add HSBK values to our colors given this canvas and our coordinates."""
        for (left_x, top_y), (tile_width, tile_height) in self.coords_and_sizes:
            self.add_tile(
                canvas.points_for_tile(left_x, top_y, tile_width, tile_height)
            )

    def get_theme_colors(self, theme: Theme) -> list[list[ThemeColor]]:
        """
        This method creates a new canvas with random points around where each tile is,
        then shuffles those points and blurs them a little. Next, it fills the gaps between
        the points and blurs the fill as well.

        The mirrors the output you get when applying a theme in the LIFX smart phone app.

        The output is a list of 1 to 5 lists of 64 HSBK values, representing 64 zones per tile
        with each list corresponding to a tile in the device chain.
        """

        canvas = Canvas()
        theme = theme.shuffled()
        theme.ensure_color()

        for (left_x, top_y), (width, height) in self.coords_and_sizes:
            canvas.add_points_for_tile(left_x, top_y, width, height, theme)
            canvas.shuffle_points()
            canvas.blur_by_distance()

        tile_canvas = Canvas()

        for (left_x, top_y), (tile_width, tile_height) in self.coords_and_sizes:
            tile_canvas.fill_in_points(canvas, left_x, top_y, tile_width, tile_height)

        tile_canvas.blur()
        self.add_tiles_from_canvas(tile_canvas)

        return self.tiles
