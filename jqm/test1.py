#!/usr/bin/python
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/(\S*)", HomeHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)

class HomeHandler(tornado.web.RequestHandler):
    def get(self,*args):
        print args
        if len(args) > 0:
            mod = args[0]
            if len(mod) <= 0:
                mod = "test1"
            mod = mod + ".html"
        else:
            mod = "test1.html"
        print self.static_url("jquery.mobile-1.4.5.min.css")
        self.render(mod)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    print options.port
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
