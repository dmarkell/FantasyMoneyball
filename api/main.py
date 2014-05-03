# Other modules in this directory
import active_stats

# Python libraries 
import datetime
import logging
import os
import re

import webapp2

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)   

class ActiveStats(Handler):

    def get(self):
        
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'
        stats = active_stats.Stats()
        output = stats.jsonify()
        self.write(output)

app = webapp2.WSGIApplication(
    [
    ('/', ActiveStats)
    ], debug=True)

