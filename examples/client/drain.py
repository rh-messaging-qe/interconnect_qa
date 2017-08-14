import optparse

from proton import Endpoint
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


class Timeout(object):
    def __init__(self, handler):
        self.registrated_handler = handler

    def on_timer_task(self, _):
        self.registrated_handler.timeout()


class DrainMessagesHandler(MessagingHandler):
    def __init__(self, address, to_send_cnt=10, to_drain_cnt=20):
        # prefetch is set to zero so that proton does not automatically issue 10 credits.
        super(DrainMessagesHandler, self).__init__(prefetch=0)
        self.conn = None
        self.sender = None
        self.receiver = None
        self.sent_count = 0
        self.received_count = 0
        self.address = address
        self.error = "Unexpected Exit"
        self.to_send_cnt = to_send_cnt
        self.to_drain_cnt = to_drain_cnt

    def timeout(self):
        self.error = "Timeout Expired: sent: %d rcvd: %d" % (self.sent_count, self.received_count)
        self.conn.close()

    def on_start(self, event):
        self.timer = event.reactor.schedule(5, Timeout(self))
        self.conn = event.container.connect(self.address)

        # Create a sender and a receiver. They are both listening on the same address
        self.receiver = event.container.create_receiver(self.conn, "pulp.task.abc")
        self.sender = event.container.create_sender(self.conn, "pulp.task.abc")
        self.receiver.flow(1)

    def on_link_flow(self, event):

        if event.link.is_sender and event.link.credit:
            print("sender credit: ", event.link.credit)

        if event.link.is_sender and event.link.credit \
                and event.link.state & Endpoint.LOCAL_ACTIVE \
                and event.link.state & Endpoint.REMOTE_ACTIVE:
            self.on_sendable(event)

        # The fact that the event.link.credit is 0 means that the receiver will not be receiving any more
        # messages. That along with 10 messages received indicates that the drain worked and we can
        # declare that the test is successful
        if self.received_count == self.to_send_cnt and event.link.credit == 0:
            self.error = None
            self.timer.cancel()
            self.receiver.close()
            self.sender.close()
            self.conn.close()

    def on_sendable(self, event):
        if self.sent_count < self.to_send_cnt:
            msg = Message(body="Hello World", properties={'seq': self.sent_count})
            dlv = event.sender.send(msg)
            dlv.settle()
            self.sent_count += 1

    def on_message(self, event):
        if event.receiver == self.receiver:
            if "Hello World" == event.message.body:
                self.received_count += 1
                print("received ", event.message.properties['seq'])

            if self.received_count < 4:
                event.receiver.flow(1)
            elif self.received_count == 4:
                # We are issuing a drain of 20. This means that we will receive all the 10 messages
                # that the sender is sending. The routers will also send back a response flow frame with
                # drain=True but I don't have any way of making sure that the response frame reached the
                # receiver
                event.receiver.drain(self.to_drain_cnt)

    def run(self):
        Container(self).run()


parser = optparse.OptionParser(usage="usage: %prog [options]",
                               description="Send messages to the supplied address.")
parser.add_option("-a", "--address", default="localhost:5672/examples",
                  help="address to which messages are sent (default %default)")
parser.add_option("-m", "--messages", type="int", default=10,
                  help="number of messages to send (default %default)")
parser.add_option("-d", "--drain-limit", type="int", default=20,
                  help="number of messages to drain (default %default)")
opts, args = parser.parse_args()

try:
    DrainMessagesHandler(address=opts.address, to_send_cnt=opts.messages, to_drain_cnt=opts.drain_limit).run()
except KeyboardInterrupt:
    pass
