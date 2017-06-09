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
from proton.reactor import Container


class MyHandler(MessagingHandler):
  def on_connection_error(self, event):
    print(1)
    super(MyHandler, self).on_connection_error(event)

  def on_rejected(self, event):
    print(2)
    super(MyHandler, self).on_rejected(event)

  def on_transport_error(self, event):
    print(3)
    super(MyHandler, self).on_transport_error(event)

  def on_link_closed(self, event):
    print(4)
    super(MyHandler, self).on_link_closed(event)

  def on_link_closing(self, event):
    print(5)
    super(MyHandler, self).on_link_closing(event)

  def on_connection_closed(self, event):
    print(6)
    super(MyHandler, self).on_connection_closed(event)

  def on_settled(self, event):
    print(7)
    super(MyHandler, self).on_settled(event)

  def on_link_error(self, event):
    print(8)
    super(MyHandler, self).on_link_error(event)

  def on_session_error(self, event):
    print(9)
    super(MyHandler, self).on_session_error(event)

  def on_released(self, event):
    print(10)
    super(MyHandler, self).on_released(event)

  def on_session_closing(self, event):
    print(11)
    super(MyHandler, self).on_session_closing(event)

  def on_connection_closing(self, event):
    print(12)
    super(MyHandler, self).on_connection_closing(event)

  def on_reactor_init(self, event):
    print(13)
    super(MyHandler, self).on_reactor_init(event)
    snd = event.container.create_sender(self.url)
    rcv = event.container.create_receiver(snd.connection, dynamic=True)
    #rcv = event.container.create_receiver('mlesko-236x.usersys.redhat.com/myManagement', dynamic=True)
    #rcv = event.container.create_receiver(snd.connection, target='myManagement', dynamic=True)
    #rcv = event.container.create_receiver(snd.connection, source='myManagement', dynamic=True)
    #rcv = event.container.create_receiver('mlesko-236x.usersys.redhat.com/myManagement') #works dpc
    #rcv = event.container.create_receiver(snd.connection)
    rcv.open()
    self.rcv = rcv

  def on_session_closed(self, event):
    print(14)
    super(MyHandler, self).on_session_closed(event)

  def __init__(self, url, messages):
    super(MyHandler, self).__init__()
    self.url = url
    self.sent = 0
    self.confirmed = 0
    self.total = messages
    self.received = 0

  def on_sendable(self, event):
    print(15)
    body = {"attributeNames": ['name', 'role', 'name']}
    properties = {"operation" : 'QUERY', 'type': 'org.amqp.management', 'name': "self",
                  'entityType': 'org.apache.qpid.dispatch.listener'}
    address = '/$management'
    #reply_to = "receiver.remote.attach.source.address"
    #reply_to = "myManagement"
    reply_to = "/"
    print('reply_to ', reply_to)
    while event.sender.credit and self.sent < self.total:
      msg = Message(id=(self.sent + 1))
      msg.body = body
      msg.properties = properties
      msg.address = address
      msg.reply_to = reply_to
      event.sender.send(msg)
      self.sent += 1
    #event.sender.detach()
    event.sender.close()
    print('sent')

  def on_accepted(self, event):
    print(16)
    self.confirmed += 1
    if self.confirmed == self.total:
      print("all messages confirmed")
      event.connection.close()

  def on_message(self, event):
    print(17)
    self.received += 1
    #print(event.__dict__)
    print(event._attrs)
    if self.received == self.total:
      event.connection.close()
      event.container.stop()

  def on_disconnected(self, event):
    print(18)
    self.sent = self.confirmed


parser = optparse.OptionParser(usage="usage: %prog [options]",
                               description="Send messages to the supplied address.")
parser.add_option("-a", "--address", default="localhost:5672/examples",
                  help="address to which messages are sent (default %default)")
parser.add_option("-m", "--messages", type="int", default=1,
                  help="number of messages to send (default %default)")
opts, args = parser.parse_args()

try:
  container = Container(MyHandler(opts.address, opts.messages))
  # container.container_id = 'myqueue'
  container.run()
except KeyboardInterrupt:
  pass
