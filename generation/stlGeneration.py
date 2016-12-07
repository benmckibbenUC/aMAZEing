# Yan Verdeja Herms
# November 2016
# CMSC 22010
# aMAZEing

import sys
import timeit
from os import path, system
from mazeGeneration import Maze

class stlMazeWriter():
    def __init__(self, maze, marble_width=10):
        self.maze = maze
        self.tileWidth = marble_width + 2

    def writeSTL(self, filename=None):
        return self.writeSTLManually()
        #return self.writeSTLFromSCAD(filename)

    # writes STL and returns the file path
    def writeSTLFromSCAD(self, filename):
        # write paths
        head, tail = path.split(path.abspath(sys.argv[0]))
        scadFilename = path.join(head, '../mazes/' + filename + '.scad')
        stlFilename = path.join(head, '../mazes/' + filename + '.stl')

        # write OpenSCAD file
        scadHeaderFilepath = path.join(head, '../resources/scadHeader.txt')
        scadHeaderFile = open(scadHeaderFilepath, 'r')
        scadHeader = scadHeaderFile.read(-1)
        scadHeaderFile.close()
        scadFile = open(scadFilename, 'w')
        scadFile.write(scadHeader)

        for row in self.maze.tiles:
            scadFile.write("\n\trender() union() {")
            for tile in row:
                x_offset = str(tile.y) + " * (" + str(self.tileWidth) + "+WALL_THICKNESS)"
                y_offset = str(self.maze.depth - tile.x - 1) + " * (" + str(self.tileWidth) + "+WALL_THICKNESS)"
                scadFile.write("\n")
                scadFile.write("\t\ttranslate([" + x_offset + ", " + y_offset + ", 0]) {\n")
                scadFile.write("\t\t\ttile(" + str(self.tileWidth) + ", u=" + str(tile.walls['U']) + ", d=" + str(tile.walls['D']) + ", l=" + str(tile.walls['L']) + ", r=" + str(tile.walls['R']) + ");\n")
                scadFile.write("\t\t}\n")
            scadFile.write("\t}\n")

        scadFile.write("\n}\n")
        scadFile.close()

        # generate STL file using OpenSCAD
        system('openscad -o ' + stlFilename + ' ' + scadFilename + ' >&- 2>&-')

        return stlFilename

    def writeSTLManually(self):
        serialMaze = self.maze.serialize()
        serialSplit = serialMaze.split('\n')

        result = 'solid aMAZEing_Maze\n'
        for j in range(1, len(serialSplit)-1):
            for i, char in enumerate(list(serialSplit[j])):
                tileStl = getTileStl(self.tileWidth, int(char, 16), i, (self.maze.depth - j))
                result += tileStl
        result += 'endsolid aMAZEing_Maze\n'
        return result

def getTileStl(tileWidth=12, hexTile=0, x=0, y=0):
    head, tail = path.split(path.abspath(sys.argv[0]))
    tileFilename = path.join(head, '../resources/tileSTL/' + str(tileWidth) + '/' + str(hexTile) + '.stl')
    tileFile = open(tileFilename)
    tileCode = tileFile.read(-1)
    tileFile.close()

    x_offset = x * (tileWidth + 2.5)
    y_offset = y * (tileWidth + 2.5)

    result = []
    for line in tileCode.split('\n'):
        if 'vertex' in line:
            #newLine = ' '.join(['      vertex', line.split()[1], line.split()[2], line.split()[3]])
            newLine = ' '.join(['      vertex', addStrings(line.split()[1], x_offset), addStrings(line.split()[2], y_offset), line.split()[3]])
            result.append(newLine)
        elif 'solid' in line:
            continue
        else:
            result.append(line)

    return '\n'.join(result)

def addStrings(string, number):
    resultNum = float(string) + number
    return str(resultNum)


if __name__ == '__main__':
    x = 25
    y = 25
    if len(sys.argv) > 2:
        x = int(sys.argv[1])
        y = int(sys.argv[2])

    newMaze = Maze(x,y)
    newMaze.generate()
    newMaze.validate()
    writer = stlMazeWriter(newMaze, 15)
    if len(sys.argv) > 3:
        if sys.argv[3] == 'scad':
            times = timeit.Timer("writer.writeSTLFromSCAD('fromSCAD')", "from __main__ import writer").repeat(1, 1)
            print('Best Average using SCAD Method: ' + str(min(times)))
        elif sys.argv[3] == 'manual':
            times = timeit.Timer("writer.writeSTLManually()", "from __main__ import writer").repeat(3, 5)
            print('Best Average using Manual STL Manipulation Method: ' + str(min(times) / 5))
    else:
        writer.writeSTL('default')
