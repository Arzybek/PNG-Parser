from pathlib import Path
import zlib


def bytes_to_int(bytes_line):
    return int.from_bytes(bytes_line, byteorder='big')


class PngParser:
    signature = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'

    def __init__(self, file_name):
        self.check_file(file_name)
        self.chunks = {}
        self.init_chunks()
        self.run()

    def check_file(self, file_name):
        if len(file_name) <= 4 or file_name[-4:] != '.png':
            raise ValueError("It's not a png file")
        else:
            self.file_name = file_name

        config = Path(self.file_name)
        if config.is_file():
            pass
        else:
            raise FileNotFoundError

        with open(self.file_name, 'rb') as file:
            file = file.read()
        if file[:8] != self.signature:
            raise TypeError(self.file_name + " is not a PNG file")

    def init_chunks(self):
        self.chunks = {}
        self.chunks['IHDR'] = None
        self.chunks['IDAT'] = []
        self.chunks['IEND'] = False
        self.chunks['PLTE'] = None

        self.chunks['tIME'] = None
        self.chunks['zTXt'] = []
        self.chunks['tEXt'] = []
        self.chunks['iTXt'] = []
        self.chunks['gAMA'] = None
        self.chunks['bKGD'] = None
        self.chunks['cHRM'] = None
        self.chunks['iCCP'] = None
        self.chunks['sBIT'] = None
        self.chunks['sRGB'] = None
        self.chunks['pHYs'] = None
        self.chunks['hIST'] = None
        self.chunks['tRNS'] = None
        self.chunks['sPLT'] = []

    def check_crc(self, bytes, chunk_type, crc):
        comp_crc = zlib.crc32(chunk_type + bytes)
        crc = bytes_to_int(crc)
        if (comp_crc != crc):
            raise Exception("Incorrect {} chunk checksum".format(chunk_type.decode('ascii')))

    def run(self):
        try:
            with open(self.file_name, 'rb') as file:
                signature = file.read(8)
                chunk_len = 4

                while chunk_len != 0:
                    chunk_len = bytes_to_int(file.read(4))
                    chunk_type = file.read(4)
                    chunk_name = chunk_type.decode('ascii')
                    if chunk_name not in self.chunks.keys():
                        self.chunks[chunk_name] = None
                    if self.chunks[chunk_name] is None:
                        self.chunks[chunk_name] = file.read(chunk_len)
                        crc = file.read(4)
                        self.check_crc(self.chunks[chunk_name], chunk_type, crc)
                    elif type(self.chunks[chunk_name]) == list:
                        chunk = file.read(chunk_len)
                        self.chunks[chunk_name].append(chunk)
                        crc = file.read(4)
                        self.check_crc(chunk, chunk_type, crc)
                    elif (chunk_name == 'IEND'):
                        self.chunks['IEND'] = True
                        crc = file.read(4)
                self.check_on_min_chunks()
        except Exception:
            raise Exception('Something is wrong')

    def check_on_min_chunks(self):
        if (self.chunks['IHDR'] is None):
            raise AttributeError('Invalid IHDR chunk')
        if (not self.chunks['IDAT']):
            raise AttributeError('Invalid IDAT chunk')
        if (not self.chunks['IEND']):
            raise AttributeError('Invalid IEND chunk')
