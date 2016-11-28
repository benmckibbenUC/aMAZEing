# Yan Verdeja Herms
# November 2016
# CMSC 22010
# aMAZEing

import sys
from os import system
from mazeGeneration import Maze

class stlMazeWriter():
    def __init__(self, maze, marble_width=10):
        self.maze = maze
        self.tileWidth = marble_width + 2

    def writeSTL(self, filename):
        # write paths
        scadFilename = '../mazes/' + filename + '.scad'
        stlFilename = '../mazes/' + filename + '.stl'

        # write OpenSCAD file
        scadHeaderFile = open('../resources/scadHeader.txt', 'r')
        scadHeader = scadHeaderFile.read(-1)
        scadHeaderFile.close()
        scadFile = open(scadFilename, 'w')
        scadFile.write(scadHeader)

        for row in self.maze.tiles:
            scadFile.write("\n\trender() union() {")
            for tile in row:
                x_offset = str(tile.y) + " * (" + str(self.tileWidth) + "+(2*WALL_THICKNESS))"
                y_offset = str(self.maze.depth - tile.x - 1) + " * (" + str(self.tileWidth) + "+(2*WALL_THICKNESS))"
                scadFile.write("\n")
                scadFile.write("\t\ttranslate([" + x_offset + ", " + y_offset + ", 0]) {\n")
                scadFile.write("\t\t\ttile(" + str(self.tileWidth) + ", u=" + str(tile.walls['U']) + ", r=" + str(tile.walls['R']) + ", d=" + str(tile.walls['D']) + ", l=" + str(tile.walls['L']) + ");\n")
                scadFile.write("\t\t}\n")
            scadFile.write("\t}\n")

        scadFile.write("\n}\n")
        scadFile.close()

        # generate STL file using OpenSCAD
        system('openscad -o ' + stlFilename + ' ' + scadFilename)

newMaze = Maze(25, 30)
newMaze.generate()
newMaze.validate()

writer = stlMazeWriter(newMaze, 12)
writer.writeSTL('test2')
