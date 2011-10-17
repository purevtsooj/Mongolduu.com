#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from google.appengine.api import urlfetch
import re
import os


class MainHandler(webapp.RequestHandler):
    def get(self):
        code = str('http://mongolduu.asuult.net/getmp3.php?ID='+self.request.get('code')).strip()
        result = urlfetch.fetch(url=code)
        rad = result.content
        st = re.findall(r'setTimeout\(.*?\)', str(rad))
        
        uri = st[0].replace("'","").replace('setTimeout("self.location=','').replace('", 9500)','')
        result = urlfetch.fetch(url=uri)
        s3 = result.content
        reg3 = re.findall(r'<source(.*?)>', str(s3))
        
        dURL = reg3[0].replace('"','').replace('src=','').strip()
        fname = os.path.basename(reg3[0].replace('"','').replace('src=','')).strip()
        
        self.response.headers['Content-Type'] = "text/xml"
        self.response.out.write('<root><url>'+dURL+'</url><name>'+fname+'</name></root><root><url>'+dURL+'</url><name>'+fname+'</name></root>')


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
