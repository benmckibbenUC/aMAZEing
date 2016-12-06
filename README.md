# aMAZEing
Final project for Digital Fabrication

=======
## Dependencies
- [Python 2.7](https://www.python.org/downloads/release/python-2712/) (no third-party package dependencies)

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
