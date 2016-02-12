#!/usr/bin/python
#
# Control URLS
# / <-- Statistics
# /haltall <-- Halt any running program, nothing will run
# /skipall <-- Stop any running programs but allow the scheduler to run
# /programs <-- All stored programs
# /programs/<pid>/detail <-- All stored programs
# /programs/<pid>/edit <-- Take a modification of a given program
# /programs/<pid>/enable <-- Enable a program to be scheduled
# /programs/<pid>/disable <-- Disable a program from being schedule
# /programs/<pid>/skip <-- Stop the program, if it is running, but allow it to be rescheduled

import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

nulls = json.dumps(None)

stats = {'rain_sensor': None, 'uptime': 5710100, 'running_program': {'active_zone': 3, 'pid': 1, 'name': 'program 1', 'time_left': 231, 'program_type': 'even'}, 'program_list': [(1, 'program 1'), (2, 'program 2'), (3, 'shifty!')], 'weather_data': None}

program_1 = {"pid": 1,
             "name" : "program 1",
             "time_of_day" : 0,
             "interval" : {"type":"even"},
             "in_program" : False,
             "station_duration" : [{"stid":1,
                                    "duration":5,
                                    "in_station":False},
                                   {"stid":2,
                                    "duration":5,
                                    "in_station":False},
                                   {"stid":3,
                                    "duration":5,
                                    "in_station":False},
                                   {"stid":4,
                                    "duration":5,
                                    "in_station":False},
                                   {"stid":5,
                                    "duration":5,
                                    "in_station":False},
                                   {"stid":6,
                                    "duration":5,
                                    "in_station":False},
                                   {"stid":7,
                                    "duration":5,
                                    "in_station":False},
                                   {"stid":8,
                                    "duration":5,
                                    "in_station":False}],
             "total_run_time":0}

class StatsHandler(tornado.web.RequestHandler):
    def get(self):
        global stats
        self.write(stats)

class ProgramDetailHandler(tornado.web.RequestHandler):
    def get(self,*args,**kwds):
        global program_1
        print args
        try:
            pid = int(args[0])
            if pid == 1:
                self.write(program_1)
            else:
                self.write(nulls)
        except ValueError:
            self.write(nulls)
    
def make_handlers():
    return [tornado.web.URLSpec(r"/",StatsHandler,name="home"),
            tornado.web.URLSpec(r"/program/([0-9]+)/detail",ProgramDetailHandler,name="p_detail")]
def make_app():
    app = tornado.web.Application(make_handlers(),
                                  debug=True)
    return app

if __name__ == "__main__":
    print "Starting "
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    print "Listening at 8080"
    tornado.ioloop.IOLoop.current().start()