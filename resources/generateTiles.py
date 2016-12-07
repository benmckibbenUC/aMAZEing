# Yan Verdeja Herms
# December 2016
# CMSC 22010
# aMAZEing

import sys
from os import path, system

class tileGenerator():
    def __init__(self, tileWidth):
        head, _ = path.split(path.abspath(sys.argv[0]))
        self.tileWidth = tileWidth
        self.directory = path.join(head, str(tileWidth))

    def makeTileStls(self):
        scadHeaderFile = open(path.join(self.directory, 'scadHeaderTile.txt'), 'r')
        scadHeader = scadHeaderFile.read(-1)
        scadHeaderFile.close()
        for i in range(0, 16):
            u = str(bool(i & 8))
            d = str(bool(i & 4))
            l = str(bool(i & 2))
            r = str(bool(i & 1))
            scadFilename = path.join(self.directory, self.tileWidth + '.scad')
            stlFilename = path.join(self.directory, self.tileWidth + '.stl')
            scadFile = open(scadFilename, 'w')
            scadFile.write(scadHeader)
            scadFile.write('tile(' + str(self.tileWidth) + ', ' + u + ', ' + d + ', ' + l + ', ' + r ')\n')
            scadFile.close()

            print('openscad -o ' + stlFilename + ' ' + scadFilename)
        print('rm ' + self.directory + '*.scad')



if __name__ == '__main__':
    generator = tileGenerator(8)
    generator.writeSCAD()
