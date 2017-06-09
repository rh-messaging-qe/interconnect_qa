import optparse

from proton import Message
from proton.reactor import Container
from proton.handlers import MessagingHandler

class Timeout(object):
  def __init__(self, handler):
    self.registrated_handler = handler

  def on_timer_task(self, _):
    self.registrated_handler.timeout()

class SenderMessageHandler(MessagingHandler):
  DESTINATION = "pulp.address"
  def __init__(self, address, matrix, count):
    # prefetch is set to zero so that proton does not automatically issue 10 credits.
    super(SenderMessageHandler, self).__init__()
    self.conn = None
    self.address = address
    self.matrix = matrix
    self.matrix_final = matrix * matrix
    self.error = False
    self.counter = 0
    self.max_messages = count
    self.done = 0

  def timeout(self):
    print("ERROR: Timeout -- Not desirable")
    self.error = True
    self.conn.close()

  def on_start(self, event):
    #self.timer = event.reactor.schedule(60, Timeout(self))
    self.timer = event.reactor.schedule(360, Timeout(self))
    self.conn = event.container.connect(self.address)
    self.senders = {} #sender - count association
    for x in xrange(self.matrix):
      for y in xrange(self.matrix):
        sender = event.container.create_sender(self.conn, '%s.%s.%s' % (self.DESTINATION, x, y))
        self.senders[sender] = 0

  def on_sendable(self, event):
    if event.sender:
      if self.senders[event.sender] < self.max_messages:
        msg = Message(body="Hello World", properties={'seq': self.senders[event.sender]})
        event.sender.send(msg)
        self.senders[event.sender] += 1
        if self.senders[event.sender] == self.max_messages:
          self.done += 1
    print("message sent for %s", event.sender.name)
    if self.done == self.matrix_final:
      self.conn.close()


  def on_connection_closed(self, event):
    import pprint
    print("STATISTICS, desired number everywhere %s" % self.max_messages)
    pprint.pprint(self.senders)
    if self.error:
      print("Test Failed")
    else:
      print("Test Succeeded")
    event.container.stop()

  def run(self):
    Container(self).run()

parser = optparse.OptionParser(usage="usage: %prog [options]",
                               description="Send messages to the supplied address.")
parser.add_option("-a", "--address", default="localhost:5672",
                  help="address to which messages are sent (default %default)")
parser.add_option("-m", "--matrix", default=10, type="int",
                  help="number which defines matrix of senders (%default means %default*%default senders) (default %default)")
parser.add_option("-c", "--count", default=10, type="int",
                  help="number of messages per sender (default %default)")
opts, args = parser.parse_args()

try:
  SenderMessageHandler(address=opts.address, matrix=opts.matrix, count=opts.count).run()
except KeyboardInterrupt:
  pass
