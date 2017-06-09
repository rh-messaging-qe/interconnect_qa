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
from proton.handlers import MessagingHandler
from proton import Timeout

## Dynamic source
## Sender created during on_link_openened and address obtained -- works everytime
from proton.reactor import Container


class Timeout(object):
    def __init__(self, handler):
        self.registrated_handler = handler

    def on_timer_task(self, event):
        self.registrated_handler.timeout(event)


class SimpleReceiverHandler(MessagingHandler):
    def __init__(self, hostname="localhost", address="test_queue", count=1):
        super(SimpleReceiverHandler, self).__init__()
        self.hostname = hostname
        self.confirmed = 0
        self.total = count
        self.received = 0
        self.error = 0
        self.receiver = None
        self.r_conn = None
        self.address = address

    def on_reactor_init(self, event):
        super(SimpleReceiverHandler, self).on_reactor_init(event)
        self.timer = event.reactor.schedule(5, Timeout(self))
        self.receiver = event.container.create_receiver(self.hostname + "/" + self.address)
        self.receiver.open()

    def timeout(self, event):
        self.error = 1
        if self.receiver is not None:
            self.receiver.close()
        event.container.stop()

    def on_message(self, event):
        self.received += 1
        if self.received == self.total:
            if self.receiver is not None:
                self.receiver.close()
        event.container.stop()

    def run(self):
        Container(self).run()
