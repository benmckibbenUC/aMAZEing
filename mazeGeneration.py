# Ben McKibben
# CMSC 22010
# aMAZEing

from random import choice, randrange
from copy import copy
import sys

directions = {
    'U': (-1,0),
    'D': (1,0),
    'L': (0,-1),
    'R': (0,1)
}

opposites = {
    'U': 'D',
    'D': 'U',
    'L': 'R',
    'R': 'L'
}

class Tile():
    # initializes a Tile with coordinates x, y and all four walls activated
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {
            'U': True,
            'D': True,
            'L': True,
            'R': True
        }
        self.visited = False
    
    # two Tiles are equal iff they have the same walls activated
    def __eq__(self, other):
        return self.walls == other.walls
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
class Maze():
    # initializes an x-by-y maze with all Tiles' walls activated
    def __init__(self, x, y):
        if x <= 0 or y <= 0:
            raise Exception('Both Maze dimensions must be greater than 0.')
        self.tiles = []
        for i in xrange(x):
            newRow = []
            for j in xrange(y):
                newRow.append(Tile(i,j))
            self.tiles.append(newRow)
        self.depth = x
        self.width = y

    # returns a visual representation of the maze
    def __str__(self, tilesize=4):
        image = []
        for i in xrange((self.depth+1) * tilesize):
            newRow = []
            for j in xrange((self.width+1) * tilesize):
                newRow.append(' ')
            image.append(newRow)
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                if tile.walls['U']:
                    for k in xrange(j*tilesize, (j+1)*tilesize):
                        image[i*tilesize][k] = '.'
                if tile.walls['D']:
                    for k in xrange(j*tilesize, (j+1)*tilesize+1):
                        image[(i+1)*tilesize][k] = '.'
                if tile.walls['L']:
                    for k in xrange(i*tilesize, (i+1)*tilesize):
                        image[k][j*tilesize] = '.'
                if tile.walls['R']:
                    for k in xrange(i*tilesize, (i+1)*tilesize+1):
                        image[k][(j+1)*tilesize] = '.'
        ret = ''
        for i in image:
            for j in i:
                ret += j
            ret += '\n'
        return ret
    
    # two Mazes are equal iff they have the same dimensions and all of their tiles are equal
    def __eq__(self, other):
        if self.depth != other.depth or self.width != other.width:
            return False
        for i in xrange(self.depth):
            for j in xrange(self.width):
                if self.tiles[i][j] != other.tiles[i][j]:
                    return False
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)

    # get random unvisited neighbor for Tile at (x,y)
    def getRandomNeighbor(self, x, y):
        selectDirs = copy(directions.keys())
        if x == 0:
            selectDirs.remove('U')
        if x == self.depth - 1:
            selectDirs.remove('D')
        if y == 0:
            selectDirs.remove('L')
        if y == self.width - 1:
            selectDirs.remove('R')
        while selectDirs:
            newDir = choice(selectDirs)
            newCoords = directions[newDir]
            newTile = self.tiles[x+newCoords[0]][y+newCoords[1]]
            if not newTile.visited:
                return newTile, newDir
            selectDirs.remove(newDir)
        return None

    # generate a new, valid puzzle for this Maze
    def generate(self):
        stack = [self.tiles[0][0]]
        while stack:
            curTile = stack[-1]
            curTile.visited = True
            neighbor = self.getRandomNeighbor(curTile.x, curTile.y)
            if not neighbor:
                stack.pop()
                continue
            curTile.walls[neighbor[1]] = False
            neighbor[0].walls[opposites[neighbor[1]]] = False
            stack.append(neighbor[0])
    
    # ensures the Maze is valid, throws AssertionError otherwise
    # a maze is valid iff both the following are true:
    # - the shared walls between two neighbor Tiles are either both activated or deactivated
    # - the walls along the edges of the maze are all activated
    def validate(self):
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                if i != 0:
                    assert tile.walls['U'] == self.tiles[i-1][j].walls['D']
                else:
                    assert tile.walls['U']
                if i != self.depth - 1:
                    assert tile.walls['D'] == self.tiles[i+1][j].walls['U']
                else:
                    assert tile.walls['D']
                if j != 0:
                    assert tile.walls['L'] == self.tiles[i][j-1].walls['R']
                else:
                    assert tile.walls['L']
                if j != self.width - 1:
                    assert tile.walls['R'] == self.tiles[i][j+1].walls['L']
                else:
                    assert tile.walls['R']

    # create a serialized representation of the Maze
    # format:
    # - first line is two integers separated by a space, representing the depth and width
    # - if the depth of the maze is x and the width of the maze is y, the next x lines each contain y hexadecimal numbers in the range (0,f)
    # - each hex number represents a tile, and its bits represent the activation status of each wall
    # - the bits represent the U, D, L, R walls in that order
    def serialize(self, filename=None):
        ret = ' '.join(map(str, [self.depth, self.width])) + '\n'
        for row in self.tiles:
            for tile in row:
                char = hex((tile.walls['U']<<3)+(tile.walls['D']<<2)+(tile.walls['L']<<1)+(tile.walls['R']<<0)).replace('0x','')
                assert len(char)==1
                ret += char
            ret += '\n'
        if filename:
            with open(filename, 'wb') as f:
                f.write(ret)
        return ret
    
    # creates a new Maze from a serialized representation of a Maze as generated by serialize()
    @staticmethod
    def deserialize(serialized):
        serialSplit = serialized.split('\n')
        dims = map(int, serialSplit[0].split())
        newMaze = Maze(dims[0], dims[1])
        for i in xrange(len(serialSplit)-1):
            curLine = serialSplit[i+1]
            for j, char in enumerate(list(curLine)):
                curTile = newMaze.tiles[i][j]
                hexTile = int(char, 16)
                curTile.walls['U'] = bool(hexTile & 8)
                curTile.walls['D'] = bool(hexTile & 4)
                curTile.walls['L'] = bool(hexTile & 2)
                curTile.walls['R'] = bool(hexTile & 1)
        return newMaze

if __name__ == '__main__':
    processed = False
    if 'generate' in sys.argv:
        try:
            index = sys.argv.index('generate')
            x = int(sys.argv[index+1])
            y = int(sys.argv[index+2])
        except ValueError:
            print 'The two parameters immediately following \'generate\' must be integers. Exiting...'
            sys.exit()
        except IndexError:
            print 'You must supply dimensions for the maze. Exiting...'
            sys.exit()
        newMaze = Maze(x,y)
        newMaze.generate()
        try:
            newMaze.validate()
        except AssertionError:
            print 'Error validating new maze. Exiting...'
            sys.exit()
        if '-f' in sys.argv:
            try:
                newMaze.serialize(sys.argv[sys.argv.index('-f')+1])
            except IndexError:
                print 'You must supply a file name to export a maze. Exiting...'
                sys.exit()
        if '-p' in sys.argv:
            print newMaze
        processed = True
    if 'runtests' in sys.argv:
        failed = 0
        tot = 2
        # test 1: generate a few arbitrary Mazes and validate them
        for i in xrange(30):
            x = randrange(1,250)
            y = randrange(1,250)
            try:
                m = Maze(x, y)
                m.generate()
                m.validate()
            except Exception as e:
                print 'Maze generation/validation test failed on size ' + str((x,y)) + '.'
                failed += 1
                break
        # test 2: serialize a few Mazes, then deserialize and assert equality
        for i in xrange(30):
            m = Maze(randrange(1,250), randrange(1,250))
            n = Maze.deserialize(m.serialize())
            try:
                assert m == n
            except AssertionError:
                print 'Maze serialization/deserialization test failed.'
                failed += 1
                break
        if failed:
            print str(failed) + ' of ' + str(tot) + ' tests failed.'
        else:
            print 'All ' + str(tot) + ' tests passed!'
        processed = True
    if not processed:
        print 'aMAZEing Maze Generation\n'
        print 'Usage:'
        print 'python mazeGeneration.py generate x y [-f filename] [-p]'
        print '    * Generates a maze of dimensions x,y (must be integers greater than 0)'
        print '    * -f: serializes the maze to filename'
        print '    * -p: prints a visual representation of the maze when it\'s done'
        print 'python mazeGeneration.py runtests'
        print '    * Runs some tests'
        print '    * Can also be run with generate'