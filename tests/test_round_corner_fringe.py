# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from tornado.testing import gen_test

from tests.base import FilterTestCase


class RoundCornerFringeTestCase(FilterTestCase):
    @gen_test
    async def test_transparent_round_corner_edge_keeps_source_color(self):
        # With the transparent flag, pixels that are still opaque inside the
        # corner arc must keep the source color. The bug darkens the opaque
        # edge pixels toward black, so they differ from the source.
        radius = 50
        source = self.get_fixture("source.jpg", mode="RGBA")
        image = await self.get_filtered(
            "source.jpg",
            "thumbor.filters.round_corner",
            "round_corner(50,255,0,0,1)",
            mode="RGBA",
        )

        darkened = []
        for y in range(radius):
            for x in range(radius):
                r, g, b, a = image.getpixel((x, y))
                if a != 255:
                    continue
                sr, sg, sb, _ = source.getpixel((x, y))
                if max(abs(r - sr), abs(g - sg), abs(b - sb)) > 3:
                    darkened.append((x, y))

        assert darkened == [], (
            f"{len(darkened)} opaque corner pixels differ from the source; "
            f"first few: {darkened[:5]}"
        )
