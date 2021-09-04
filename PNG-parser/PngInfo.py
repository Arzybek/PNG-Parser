from PngParser import bytes_to_int
import zlib


class PngInfo:
    type_of_pngs = {'0': 'Greyscale', '2': 'Truecolor', '3': 'Indexed color', '4': 'Greyscale with alpha',
                    '6': 'Truecolour with alpha'}
    colour_bit_table = {'0': [1, 2, 4, 8, 16], '2': [8, 16], '3': [1, 2, 4, 8], '4': [8, 16], '6': [8, 16]}
    interlace_table = {'0': "no interlace", '1': "Adam7 interlace"}

    def __init__(self, chunks, flag):
        self.chunks = chunks
        self.info = {}
        self.parse_critical()
        self.parse_ancillary()
        self.set_info()
        self.print_info()
        self.full_flag = flag

    def parse_ancillary(self):
        self.parse_time()
        self.parse_text()
        self.parse_gama()
        self.parse_background_color()
        self.parse_chromaticities()
        self.parse_iccup()
        self.parse_sbit()
        self.parse_srgb()
        self.set_phys()
        self.set_histogram()
        self.set_transparency()
        self.set_suggested_palette()

    def print_info(self):
        for one in self.str_info:
            print(one)

    def bytes_to_int(self, bytes_line):
        return int.from_bytes(bytes_line, byteorder='big')

    def set_info(self):
        strList = []
        strList.append('Image is {} type PNG'.format(self.info['PNG']))
        a = [self.info['IHDR']['width'], self.info['IHDR']['height'], self.info['IHDR']['bit_depth'],
             self.info['IHDR']['type_of_color'], self.info['IHDR']['method_of_compression'],
             self.info['IHDR']['method_of_filtration'], self.info['IHDR']['interlace']]
        strList.append('Width: {} \n'
                       'Height: {} \n'
                       'Bit depth: {} \n'
                       'Type of color: {} \n'
                       'Method of compression: {} \n'
                       'Method of filtration: {} \n'
                       'Interlace: {}'.format(*a))
        if ('tEXt' in self.info.keys()):
            strList.append('tEXt information:')
            for key, value in self.info['tEXt'].items():
                strList.append('{}: {}'.format(key, value))
        if ('zTXt' in self.info.keys()):
            strList.append('zTXt information:')
            for key, value in self.info['zTXt'].items():
                strList.append('{}: {}'.format(key, value))
        if ('iTXt' in self.info.keys()):
            strList.append('iTXt information:')
            for one in self.info['iTXt']:
                for key, value in one.items():
                    strList.append('{}: {}'.format(key, value))
        if ('tIME' in self.info.keys()):
            strList.append('tIME info: {}'.format(self.info['tIME']))
        if ('gAMA' in self.info.keys()):
            strList.append('Gamma: {}'.format(self.info['gAMA']))
        if ('cHRM' in self.info.keys()):
            strList.append('Chromaticities: {}'.format(self.info['cHRM']))
        if ('sBIT' in self.info.keys()):
            dict = self.info['sBIT']
            strList.append('sBIT information:')
            for key, value in dict.items():
                strList.append("{} : {}".format(key, value))
        if ('bKGD' in self.info.keys()):
            strList.append('bKGD information:')
            strList.append(self.info['bKGD'])
        if ('sRGB' in self.info.keys()):
            strList.append("sRGB colour space: {}".format(self.info['sRGB']))
        if ('pHYs' in self.info.keys()):
            strList.append("Physical pixel dimensions: ")
            strList.append(self.info['pHYs'])
        if ('hIST' in self.info.keys()):
            strList.append("Length of histogram: {}".format(len(self.info['hIST'])))
        if ('tRNS' in self.info.keys()):
            strList.append("Transparency info")
            strList.append(self.info['tRNS'])
        if ('sPLT' in self.info.keys()):
            strList.append("Suggested palette info:")
            for palette in self.info['sPLT']:
                strList.append(palette)
        self.str_info = strList

    def parse_critical(self, *args):
        self.info['IEND'] = "True"
        if ('PLTE' in self.chunks.keys()):
            self.info['PLTE'] = str(self.chunks['PLTE'])
        self.info['IDAT'] = str(self.chunks['IDAT'])

        bit_depth = self.chunks['IHDR'][8]
        type_of_color = self.chunks['IHDR'][9]
        method_of_compression = self.chunks['IHDR'][10]
        method_of_filtration = self.chunks['IHDR'][11]
        interlace = self.chunks['IHDR'][12]

        self.info['PNG'] = self.type_of_pngs[str(type_of_color)]
        if (bit_depth not in self.colour_bit_table[str(type_of_color)]):
            raise Exception('Wrong combination of colour and bit_depth')
        if (method_of_filtration or method_of_compression != 0):
            raise Exception('Method of filtration/compression is not correct')

        info = {}
        info['width'] = self.bytes_to_int(self.chunks['IHDR'][:4])
        info['height'] = self.bytes_to_int(self.chunks['IHDR'][4:8])
        info['bit_depth'] = self.chunks['IHDR'][8]
        info['type_of_color'] = self.chunks['IHDR'][9]
        info['method_of_compression'] = "0 / Deflate"
        info['method_of_filtration'] = "0 / Adaptive filtering with five basic filter types"
        info['interlace'] = "{} / {}".format(interlace, self.interlace_table[str(interlace)])
        self.info['IHDR'] = info

    def parse_time(self):
        if self.chunks['tIME'] is not None:
            year = self.bytes_to_int(self.chunks['tIME'][:2])
            month = self.chunks['tIME'][2]
            day = self.chunks['tIME'][3]
            hour = self.chunks['tIME'][4]
            minute = self.chunks['tIME'][5]
            second = self.chunks['tIME'][6]
            self.info['tIME'] = '{}.{}.{} {}:{}:{}'.format(day, month, year, hour, minute, second)

    def parse_text(self):
        if (len(self.chunks['tEXt']) != 0):
            self.info['tEXt'] = {}
            for chunk in self.chunks['tEXt']:
                keyword, text_string = chunk.split(b'\x00')
                self.info['tEXt'][keyword.decode('latin-1')] = text_string.decode('latin-1')
        if (len(self.chunks['zTXt']) != 0):
            self.info['zTXt'] = {}
            for chunk in self.chunks['zTXt']:
                keyword, data_stream = chunk.split(b'\x00\x00')
                data_stream = zlib.decompress(data_stream)
                self.info['zTXt'][keyword.decode('latin-1')] = data_stream.decode('latin-1')
        if (len(self.chunks['iTXt']) != 0):
            self.info['iTXt'] = []
            for chunk in self.chunks['iTXt']:
                null = chunk.index(b'\x00')
                keyword = chunk[:null]
                compression_flag = chunk[null + 1]
                compression_method = chunk[null + 2]
                null += 3
                chunk = chunk[null:]
                null = chunk.index(b'\x00')
                lang_tag = chunk[:null]
                if (lang_tag != b''):
                    lang_tag = lang_tag.decode('utf-8')
                else:
                    lang_tag = None
                chunk = chunk[null + 1:]
                null = chunk.index(b'\x00')
                trans_keyword = chunk[:null]
                if (trans_keyword != b''):
                    trans_keyword = trans_keyword.decode('utf-8')
                else:
                    trans_keyword = None
                text = chunk[null + 1:]
                if (text == b''):
                    text = None
                elif (compression_flag == 1):
                    text = zlib.decompress(text).decode('utf-8')
                text = text.decode('utf-8')
                dict = {"keyword": keyword, "language tag": lang_tag, "translated keyword": trans_keyword,
                        "text": text}
                self.info['iTXt'].append(dict)

    def parse_unknown(self):
        for key in self.chunks.keys():
            if (key not in self.info.keys()):
                if (key[0].isupper()):
                    raise Exception("PNG information can't safely interpret")
                self.info[key] = self.chunks[key]

    def parse_gama(self):
        if (self.chunks['gAMA'] != None):
            self.info['gAMA'] = round(bytes_to_int(self.chunks['gAMA']) / 100000, 5)

    def parse_srgb(self):
        if (self.chunks['sRGB'] != None):
            dict = {0: "Perceptual", 1: "Relative colorimetric", 2: "Saturation", 3: "Absolute colorimetric"}
            self.info['sRGB'] = dict[bytes_to_int(self.chunks['sRGB'])]

    def parse_background_color(self):
        if (self.chunks['bKGD'] != None):
            color = self.info['IHDR']['type_of_color']
            chunk = self.chunks['bKGD']
            if (color == 0 or 4):
                self.info['bKGD'] = {"Greyscale": bytes_to_int(chunk)}
            if (color == 2 or 6):
                self.info['bKGD'] = {"Red": bytes_to_int(chunk[0:2]),
                                     "Green": bytes_to_int(chunk[2:4]),
                                     "Blue": bytes_to_int(chunk[4:2])}
            if (color == 3):
                self.info['bKGD'] = {"Palette index": bytes_to_int(chunk)}

    def parse_chromaticities(self):
        if (self.chunks['cHRM'] != None):
            self.info['cHRM'] = {}
            chunk = self.chunks['cHRM']
            dict = self.info['cHRM']
            dict['White x'] = bytes_to_int(chunk[:4]) / 100000
            dict['White y'] = bytes_to_int(chunk[4:8]) / 100000
            dict['Red x'] = bytes_to_int(chunk[8:12]) / 100000
            dict['Red y'] = bytes_to_int(chunk[12:16]) / 100000
            dict['Green x'] = bytes_to_int(chunk[16:20]) / 100000
            dict['Green y'] = bytes_to_int(chunk[20:24]) / 100000
            dict['Blue x'] = bytes_to_int(chunk[24:28]) / 100000
            dict['Blue y'] = bytes_to_int(chunk[28:32]) / 100000

    def parse_iccup(self):
        if (self.chunks['iCCP'] != None):
            splitted_chunk = self.chunks['iCCP'].split(b'\x00\x00', 1)
            name, profile = splitted_chunk[0], splitted_chunk[1]
            name = name.decode('latin-1')
            profile = zlib.decompress(profile)
            self.info['iCCP'] = {'Name': name, 'Profile': profile}

    def parse_sbit(self):
        if (self.chunks['sBIT'] != None):
            color_type = self.info['IHDR']['type_of_color']
            dict = {}
            if (color_type == 0):
                dict['greyscale'] = self.chunks['sBIT']
            if (color_type == 2 or 3):
                dict = {'red': 0, 'green': 0, 'blue': 0}
                dict['red'] = self.chunks['sBIT'][0]
                dict['green'] = self.chunks['sBIT'][1]
                dict['blue'] = self.chunks['sBIT'][2]
            if (color_type == 4):
                dict = {'greyscale': 0, 'alpha': 0}
                dict['greyscale'] = self.chunks['sBIT'][0]
                dict['alpha'] = self.chunks['sBIT'][1]
            if (color_type == 6):
                dict = {'red': 0, 'green': 0, 'blue': 0, 'alpha': 0}
                dict['red'] = self.chunks['sBIT'][0]
                dict['green'] = self.chunks['sBIT'][1]
                dict['blue'] = self.chunks['sBIT'][2]
                dict['alpha'] = self.chunks['sBIT'][3]
            for key in dict.keys():
                if (dict[key] < 0 or dict[key] > self.info['IHDR']['bit_depth']):
                    raise Exception('Wrong sBIT chunk')
            self.info['sBIT'] = dict

    def set_phys(self):
        if (self.chunks['pHYs'] != None):
            dict = {}
            unit_specifier = {0: "unknown", 1: "the metre"}
            dict['ppu X'] = bytes_to_int(self.chunks['pHYs'][0:4])
            dict['ppu Y'] = bytes_to_int(self.chunks['pHYs'][4:8])
            us = self.chunks['pHYs'][8]
            dict['unit'] = (unit_specifier[us], us)
            self.info['pHYs'] = dict

    def set_histogram(self):
        if (self.chunks['hIST'] != None):
            chunk = self.chunks['hIST']
            list = [chunk[i:i + 2] for i in range(0, len(chunk), 2)]
            for i in range(len(list)):
                list[i] = bytes_to_int(list[i])
            self.info['hIST'] = list

    def set_transparency(self):
        if (self.chunks['tRNS'] != None):
            color_type = self.info['IHDR']['type_of_color']
            chunk = self.chunks['tRNS']
            if (color_type == 0):
                self.info['tRNS'] = {"Grey sample value": bytes_to_int(chunk[0:2])}
            if (color_type == 2):
                self.info['tRNS'] = {"Red sample value": bytes_to_int(chunk[0:2]),
                                     "Blue sample value": bytes_to_int(chunk[2:4]),
                                     "Green sample value": bytes_to_int(chunk[4:6])}
            if (color_type == 3):
                list = [bytes_to_int(chunk[i:i + 1]) for i in range(len(chunk))]
                self.info['tRNS'] = []
                for i in range(len(list)):
                    self.info['tRNS'].append("Alpha for palette index {}: {}".format(i, list[i]))

    def set_suggested_palette(self):
        if (len(self.chunks['sPLT']) != 0):
            self.info['sPLT'] = []
            for palette in self.chunks['sPLT']:
                null = palette.index(b'\x00')
                name = palette[:null].decode('latin-1')
                depth = palette[null + 1]
                palette = palette[null + 2:]
                length = 6 if depth == 8 else 10
                byte = True if depth == 8 else False
                i = 0
                while True:
                    one = palette[length * i:length * (i + 1)]
                    if one == b'':
                        break
                    red = one[0] if byte else bytes_to_int(one[:2])
                    green = one[1] if byte else bytes_to_int(one[2:4])
                    blue = one[2] if byte else bytes_to_int(one[4:6])
                    alpha = one[3] if byte else bytes_to_int(one[6:8])
                    frequency = bytes_to_int(one[4:]) if byte else bytes_to_int(one[8:])
                    dict = {'name': name, "depth": depth, "red": red, "green": green, "blue": blue, "alpha": alpha,
                            "frequency": frequency}
                    self.info['sPLT'].append(dict)
                    i += 1
