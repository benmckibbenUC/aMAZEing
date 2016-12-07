# aMAZEing
Final project for Digital Fabrication

=======
## Dependencies
- [Python 2.7](https://www.python.org/downloads/release/python-2712/) (no third-party package dependencies)

## Included Files
- [`generation`](generation)
  - [`HTTPServer.py`](generation/HTTPServer.py): Code for the maze and STL generation server.
  - [`mazeGeneration.py`](generation/mazeGeneration.py): Classes that define and generate mazes and their components. Can also be run as a script: `python mazeGeneration.py` will print a help message detailing the commands you can run to use this module for stand-alone generation.
  - [`stlGeneration.py`](generation/stlGeneration.py): Classes that work with the [`Maze`](generation/mazeGeneration.py#L43) class to generate STL files.
- [`mazes`](mazes)
  - [`modules`](mazes/modules)
    - [`tiles.scad`](mazes/modules/tiles.scad): OpenSCAD module for concave tile object
    - [`tiles2.scad`](mazes/modules/tiles2.scad): OpenSCAD module for simple tile object with walls
- [`resources`](resources)
  - [`tileSTL`](resources/tileSTL): STL files for all 16 kinds of tiles per marble size
  - [`generateTiles.py`](resources/generateTiles.py): Creates the STL files for all possible tiles

## Server Usage
```
cd generation
python HTTPServer.py
```
This starts the HTTP server for generating mazes and STL files for mazes.
### Valid Routes
- `GET /generate`: requires two query parameters, `d` and `w`, which are integers that specify the depth and width of the desired maze, respectively. Returns plaintext serialization of a maze as defined in [`Maze.serialize()`](generation/mazeGeneration.py#L157).
  - Example: `host:port/generate/?d=3&w=3`
- `POST /stl`: requires the parameter `maze`, which is a serialized maze in the format given by [`Maze.serialize()`](generation/mazeGeneration.py#L157). Also accepts an additional parameter `marble`, which is an integer that specifies the width of the tracks in the generated maze model (defaults to 10).

## iOS Companion App
The [iOS app](https://github.com/eeevanbbb/Maze4Daze) fetches new mazes from the server, simulates them on the device, and allows the user to adjust parameters and send to the printer.

## STL Generation
The STL generation file contains two STL writing methods:
  - `writeSTLFromSCAD`: creates an OpenSCAD file of the maze and then renders it with OpenSCAD
  - `writeSTLManually`: directly generates the text for an STL file from the base tiles found in resources/tileSTL
