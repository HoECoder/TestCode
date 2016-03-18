import glob
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

templates = os.path.join(os.path.dirname(__file__), "template")
statics = os.path.join(os.path.dirname(__file__), "static")

def test_file_list():
    glob_path = os.path.join(templates,"*.html")
    globs = glob.glob(glob_path)
    if len(globs) > 0:
        globs = map(lambda x: os.path.basename(x),globs)
        paths = [path[:-5] for path in globs]
        return paths
    else:
        return []

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/(\S*)", HomeHandler),
        ]
        settings = dict(
            template_path=templates,
            static_path=statics,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)

class HomeHandler(tornado.web.RequestHandler):
    def get(self,*args):
        file_list = test_file_list()
        print file_list
        if len(args) > 0:
            mod = args[0]
            if len(mod) <= 0:
                mod = "index"
            if mod == "index":
                self.render("index.html",links=file_list)
            mod = mod + ".html"
            self.render(mod)
        else:
            self.render("index.html",links=file_list)
        

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    print options.port
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
