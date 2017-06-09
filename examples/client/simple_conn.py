import optparse

from proton.reactor import Container
from proton.handlers import MessagingHandler

class Timeout(object):
  def __init__(self, handler):
    self.registrated_handler = handler

  def on_timer_task(self, _):
    self.registrated_handler.timeout()

class ShutDownMessageHandler(MessagingHandler):
  def __init__(self, address):
    # prefetch is set to zero so that proton does not automatically issue 10 credits.
    super(ShutDownMessageHandler, self).__init__(prefetch=0)
    self.conn = None
    self.address = address
    self.error = False

  def timeout(self):
    print("ERROR: Timeout -- Not desirable")
    self.error = True
    self.conn.close()

  def on_start(self, event):
    self.timer = event.reactor.schedule(5, Timeout(self))
    self.conn = event.container.connect(self.address)

  def on_connection_closed(self, event):
    if self.error:
      print("Test Failed")
    else:
      print("Test Succeeded")

  def run(self):
    Container(self).run()

parser = optparse.OptionParser(usage="usage: %prog [options]",
                               description="Send messages to the supplied address.")
parser.add_option("-a", "--address", default="localhost:5672/examples",
                  help="address to which messages are sent (default %default)")
opts, args = parser.parse_args()

try:
  ShutDownMessageHandler(address=opts.address).run()
except KeyboardInterrupt:
  pass
