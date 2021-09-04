import unittest
from PngParser import PngParser
from PngInfo import PngInfo


class ParserTestCase(unittest.TestCase):
    def test_simple_name(self):
        with self.assertRaises(ValueError):
            PngParser("asdf.pn")
        with self.assertRaises(ValueError):
            PngParser(".png")

    def test_file(self):
        with self.assertRaises(FileNotFoundError):
            PngParser("asdf.png")
        with self.assertRaises(TypeError):
            PngParser("pictures/fake_png.png")

    def test_crc(self):
        with self.assertRaises(Exception):
            PngParser("pictures/idat_crc_wrong.png")


class InfoTestCase(unittest.TestCase):
    def test_hist(self):
        png_file = PngParser("pictures/hist.png")
        png_info = PngInfo(png_file.chunks, True)
        self.assertEqual(len(png_info.info['hIST']), 256)

    def test_gamma(self):
        png_file = PngParser("pictures/gamma.png")
        png_info = PngInfo(png_file.chunks, True)
        self.assertEqual(png_info.info['gAMA'], 2.5)

    def test_chroma(self):
        png_file = PngParser("pictures/chroma.png")
        png_info = PngInfo(png_file.chunks, True)
        chunk = png_info.info['cHRM']
        self.assertEqual(chunk['White x'], 0.3127)
        self.assertEqual(chunk['White y'], 0.329)
        self.assertEqual(chunk['Red x'], 0.64)
        self.assertEqual(chunk['Red y'], 0.33)
        self.assertEqual(chunk['Green x'], 0.3)
        self.assertEqual(chunk['Green y'], 0.6)
        self.assertEqual(chunk['Blue x'], 0.15)
        self.assertEqual(chunk['Blue y'], 0.06)

    def test_ztxt(self):
        png_file = PngParser("pictures/ztxt.png")
        png_info = PngInfo(png_file.chunks, True)
        self.assertEqual(png_info.info['zTXt']['Disclaimer'], "Freeware.")

    def test_phys(self):
        png_file = PngParser("pictures/phys.png")
        png_info = PngInfo(png_file.chunks, True)
        chunk = png_info.info['pHYs']
        self.assertEqual(chunk['ppu X'], 1000)
        self.assertEqual(chunk['ppu Y'], 1000)
        self.assertEqual(chunk['unit'], ('the metre',1))

    def test_sbit(self):
        png_file = PngParser("pictures/sbit.png")
        png_info = PngInfo(png_file.chunks, True)
        chunk = png_info.info['sBIT']
        self.assertEqual(chunk['red'], 13)
        self.assertEqual(chunk['green'], 13)
        self.assertEqual(chunk['blue'], 13)
