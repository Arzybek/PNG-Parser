import argparse
from PngParser import  PngParser
from PngInfo import  PngInfo
from window import  Window
from  PyQt5 import  QtWidgets
import sys

def createParser():
    parser = argparse.ArgumentParser(
        description='Парсер PNG формата.'
    )
    parser.add_argument('-f', '--file',
                        required=True, help='Файл формата PNG.')
    parser.add_argument('-g', '--gui', help='GUI', action='store_true')
    parser.add_argument('-i', '--info', help='With this flag gives the full info about picture', action='store_true')
    return parser

if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args()
    file = namespace.file
    gui_flag = namespace.gui
    png_file = PngParser(file)
    png_info = PngInfo(png_file.chunks, namespace.info)
    if(gui_flag):
        app = QtWidgets.QApplication(sys.argv)
        ex = Window(file)
        sys.exit(app.exec_())