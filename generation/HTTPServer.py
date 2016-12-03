# Ben McKibben
# CMSC 22010
# aMAZEing

import time
import BaseHTTPServer
from random import randrange
from urlparse import urlparse, parse_qs
from mazeGeneration import Maze
from stlGeneration import stlMazeWriter

HOST_NAME = 'localhost'
PORT_NUMBER = 8080

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def send404(s):
        s.send_response(404)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>404 | aMAZEing Maze Generator</title></head>")
        s.wfile.write("<p>Sorry, page not found.</p>")
        s.wfile.write("</body></html>")

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()    

    def do_GET(s):
        """Respond to a GET request."""
        if s.path.startswith('/generate'):
            query = parse_qs(urlparse(s.path).query)
            if 'd' in query and 'w' in query:
                try:
                    newMaze = Maze(int(query['d'][0]), int(query['w'][0]))
                    newMaze.generate()
                    newMaze.validate()
                    s.wfile.write(newMaze.serialize())
                except Exception as e:
                    s.wfile.write(str(e)+'\n')
                    s.wfile.write('Recieved parameters:\n')
                    s.wfile.write(str(query))
                return   
            else:
                s.wfile.write('Missing d and w query parameters.')
                return
        s.send404()

    def do_POST(s):
        """Respond to a POST request."""
        # respond to POST request with "maze" and possible "marble" as form parameters
        if s.path.startswith('/stl'):
            raw_data = s.rfile.read(int(s.headers['Content-Length']))
            post_data = json.loads(raw_data)
            try:
                maze_serialized = post_data['maze']
            except KeyError:
                s.wfile.write('No maze recieved.')
                return
            try:
                marble_width = post_data['marble']
            except KeyError:
                marble_width = 10
            try:
                maze = Maze.deserialize(maze_serialized)
                writer = stlMazeWriter(maze, marble_width)
                filename = str(randrange(0,10000)) # get random filename
                path = writer.writeSTL(filename)
                with open(path, 'rb') as stlFile:
                    s.wfile.write(stlFile.read())
                return
            except Exception as e:
                s.wfile.write(str(e)+'\n')
                s.wfile.write('Recieved parameters:\n')
                s.wfile.write(maze_serialized + '\n')
                s.wfile.write('Marble width (defaults to 10): ' + str(marble_width))
            return
        s.send404()

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)