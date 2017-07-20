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
from proton import Timeout
from proton.handlers import MessagingHandler
from proton.reactor import Container


## Dynamic source
## Sender created during on_link_openened and address obtained -- works everytime

class Timeout(object):
    def __init__(self, handler):
        self.registrated_handler = handler

    def on_timer_task(self, event):
        self.registrated_handler.timeout(event)


class MyHandler(MessagingHandler):
    def __init__(self, url, messages):
        super(MyHandler, self).__init__()
        self.url = url
        self.sent = 0
        self.confirmed = 0
        self.total = messages
        self.received = 0
        self.sender = None
        self.receiver = None
        self.r_conn = None
        self.address = None

    def on_reactor_init(self, event):
        super(MyHandler, self).on_reactor_init(event)
        self.timer = event.reactor.schedule(5, Timeout(self))
        # self.r_conn = event.container.connect(self.url)
        # self.receiver = event.container.create_receiver(self.r_conn, dynamic=True) #works dpc
        self.receiver = event.container.create_receiver(self.url, dynamic=True)  # works dpc
        self.receiver.open()

    def timeout(self, event):
        print("TIMEOUT called, closing connections")
        self.close_all(event=event)

    def close_all(self, event):
        if self.sender is not None:
            self.sender.close()
        if self.receiver is not None:
            self.receiver.close()
        event.container.stop()

    def on_link_opened(self, event):
        if event.receiver == self.receiver:
            self.address = self.receiver.remote_source.address
            print("address is: %s" % self.address)
            self.sender = event.container.create_sender(self.receiver.connection, target=self.address)

    def on_sendable(self, event):
        while event.sender.credit and self.sent < self.total:
            msg = Message(id=(self.sent + 1))
            msg.body = self.sent
            # msg.address = address
            # msg.reply_to = reply_to
            event.sender.send(msg)
            self.sent += 1

    def on_accepted(self, event):
        self.confirmed += 1
        if self.confirmed == self.total:
            print("all messages confirmed")

    def on_message(self, event):
        self.received += 1
        print(event._attrs)
        if self.received == self.total:
            print("all messages received, closing all")
            self.close_all(event)


parser = optparse.OptionParser(usage="usage: %prog [options]",
                               description="Send messages to the supplied address.")
parser.add_option("-a", "--address", default="localhost:5672/examples",
                  help="address to which messages are sent (default %default)")
parser.add_option("-m", "--messages", type="int", default=1,
                  help="number of messages to send (default %default)")
opts, args = parser.parse_args()

try:
    container = Container(MyHandler(opts.address, opts.messages))
    container.run()
except KeyboardInterrupt:
    pass
