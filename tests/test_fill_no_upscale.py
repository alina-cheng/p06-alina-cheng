# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from io import BytesIO
from os.path import dirname, join, realpath

from PIL import Image
from tornado.testing import gen_test

from tests.base import TestCase
from thumbor.config import Config


class FillNoUpscaleTestCase(TestCase):
    def get_config(self):
        config = Config()
        config.LOADER = "thumbor.loaders.file_loader"
        config.FILE_LOADER_ROOT_PATH = join(
            dirname(realpath(__file__)), "fixtures", "images"
        )
        config.FILTERS = [
            "thumbor.filters.fill",
            "thumbor.filters.no_upscale",
        ]
        return config

    @gen_test
    async def test_fill_then_no_upscale_keeps_canvas(self):
        response = await self.async_get(
            "/unsafe/fit-in/300x300/filters:fill(red):no_upscale()/20x20.jpg"
        )
        image = Image.open(BytesIO(response.body))
        assert image.size == (300, 300), image.size

    @gen_test
    async def test_no_upscale_then_fill_keeps_canvas(self):
        response = await self.async_get(
            "/unsafe/fit-in/300x300/filters:no_upscale():fill(red)/20x20.jpg"
        )
        image = Image.open(BytesIO(response.body))
        assert image.size == (300, 300), image.size

    @gen_test
    async def test_fill_then_no_upscale_with_orig_width_returns_image(self):
        response = await self.async_get(
            "/unsafe/fit-in/origx300/filters:fill(red):no_upscale()/20x20.jpg"
        )
        assert response.code == 200, response.code
        Image.open(BytesIO(response.body))

    @gen_test
    async def test_no_upscale_then_fill_with_orig_width_returns_image(self):
        response = await self.async_get(
            "/unsafe/fit-in/origx300/filters:no_upscale():fill(red)/20x20.jpg"
        )
        assert response.code == 200, response.code
        Image.open(BytesIO(response.body))
