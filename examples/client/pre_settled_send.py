#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import print_function, unicode_literals

import optparse

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import AtMostOnce
from proton.reactor import Container


class Send(MessagingHandler):
    def __init__(self, url, messages):
        super(Send, self).__init__()
        self.url = url
        self.sent = 0
        self.confirmed = 0
        self.total = messages

    def on_start(self, event):
        event.container.create_sender(self.url, options=AtMostOnce())

    def on_sendable(self, event):
        while event.sender.credit and self.sent < self.total:
            # msg = Message(id=(self.sent+1), body={'sequence':(self.sent+1)}, address="pulp")
            msg = Message(id=(self.sent + 1), body={'sequence': (self.sent + 1)}, address="pulp.task")
            event.sender.send(msg)
            self.sent += 1
        if self.sent == self.total:
            print("all messages sent")
            event.connection.close()
            event.container.stop()
            exit()


parser = optparse.OptionParser(usage="usage: %prog [options]",
                               description="Send messages to the supplied address.")
parser.add_option("-a", "--address", default="localhost:5672/examples",
                  help="address to which messages are sent (default %default)")
parser.add_option("-m", "--messages", type="int", default=100,
                  help="number of messages to send (default %default)")
opts, args = parser.parse_args()

try:
    container = Container(Send(opts.address, opts.messages))
    container.container_id = 'pre-settled sender'
    container.run()
except KeyboardInterrupt:
    pass
