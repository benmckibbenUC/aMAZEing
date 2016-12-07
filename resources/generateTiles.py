# Yan Verdeja Herms
# December 2016
# CMSC 22010
# aMAZEing

import sys
from os import path, system, makedirs

class tileGenerator():
    def __init__(self, tileWidth):
        head, _ = path.split(path.abspath(sys.argv[0]))
        self.tileWidth = tileWidth
        self.directory = path.join(head, 'tileSTL/' + str(tileWidth))
        if not path.exists(self.directory):
            makedirs(self.directory)
        headerFile = open(path.join(head, 'scadHeaderTile.txt'), 'r')
        self.header = headerFile.read(-1)
        headerFile.close()

    def makeTileStls(self):
        for i in range(0, 16):
            u = str(bool(i & 8))
            d = str(bool(i & 4))
            l = str(bool(i & 2))
            r = str(bool(i & 1))
            scadFilename = path.join(self.directory, str(i) + '.scad')
            stlFilename = path.join(self.directory, str(i) + '.stl')
            scadFile = open(scadFilename, 'w')
            scadFile.write(self.header)
            scadFile.write('\ntile(' + str(self.tileWidth) + ', ' + u + ', ' + d + ', ' + l + ', ' + r + ');\n')
            scadFile.close()

            system('openscad -o ' + stlFilename + ' ' + scadFilename)
        system('rm ' + self.directory + '/*.scad')



if __name__ == '__main__':
    for i in range(0, 26):
        generator = tileGenerator(i)
        generator.makeTileStls()
