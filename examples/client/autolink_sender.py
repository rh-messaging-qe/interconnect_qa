import optparse

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


class Timeout(object):
    def __init__(self, handler):
        self.registrated_handler = handler

    def on_timer_task(self):
        self.registrated_handler.timeout()


class Sender(object):
    def __init__(self, msg_cnt, address_name):
        self.msg_cnt = msg_cnt
        self.address_name = address_name


class SenderMessageHandler(MessagingHandler):
    DESTINATION = "pulp.address"

    def __init__(self, address, sender_cnt, count):
        # prefetch is set to zero so that proton does not automatically issue 10 credits.
        super(SenderMessageHandler, self).__init__()
        self.conn = None
        self.address = address
        self.sender_cnt = sender_cnt
        self.error = False
        self.counter = 0
        self.max_messages = count
        self.done = 0

    def on_start(self, event):
        self.conn = event.container.connect(self.address)
        self.senders = {}  # sender - count association
        for x in xrange(self.sender_cnt):
            sender = event.container.create_sender(self.conn)
            self.senders[sender] = Sender(msg_cnt=0, address_name=x)

    def on_sendable(self, event):
        if event.sender:
            sender = self.senders[event.sender]
            if sender.msg_cnt < self.max_messages:
                msg = Message(address='%s.%s' % (self.DESTINATION, sender.address_name), body="Hello World",
                              properties={'seq': sender.msg_cnt})
                event.sender.send(msg)
                sender.msg_cnt += 1
                if sender.msg_cnt == self.max_messages:
                    self.done += 1
        print("message sent for %s", event.sender.name)
        if self.done == self.sender_cnt:
            self.conn.close()

    def on_connection_closed(self, event):
        import pprint
        print("STATISTICS, desired number everywhere %s" % self.max_messages)
        for x in self.senders.itervalues():
            pprint.pprint("address %s, msg_count: %s" % (x.address_name, x.msg_cnt))
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
parser.add_option("-s", "--senders", default=2, type="int",
                  help="number which defines matrix of senders (%default means %default*%default senders) (default %default)")
parser.add_option("-c", "--count", default=10, type="int",
                  help="number of messages per sender (default %default)")
opts, args = parser.parse_args()

try:
    SenderMessageHandler(address=opts.address, sender_cnt=opts.senders, count=opts.count).run()
except KeyboardInterrupt:
    pass
