# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

__author__ = 'Damon Kohler <damonkohler@gmail.com>'

import json
import os
import socket
import sys

PORT = os.environ.get('AP_PORT')


class Android(object):

  def __init__(self):
    self.conn = socket.create_connection(('localhost', PORT))
    self.client = self.conn.makefile()
    self.id = 0

  def _rpc(self, method, *args):
    data = {'id': self.id,
            'method': method,
            'params': args}
    request = json.dumps(data)
    self.client.write(request+'\n')
    self.client.flush()
    response = self.client.readline()
    self.id += 1
    result = json.loads(response)
    if result['error'] is not None:
      print result['error']
    return result

  def __getattr__(self, name):
    def rpc_call(*args):
      return self._rpc(name, *args)
    return rpc_call

  def help(self, method=None):
    if method is None:
      help = self._help()
    else:
      help = self._help(method)
    if help['error'] is not None:
      print 'Failed to retrieve help text.'
    else:
      for m in help['result']:
        print m