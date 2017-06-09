from proton import Message
from proton.reactor import Container
from proton.handlers import MessagingHandler


class Timeout(object):
    def __init__(self, handler):
        self.registrated_handler = handler

    def on_timer_task(self, _):
        self.registrated_handler.timeout()


class SimpleSenderHandler(MessagingHandler):
    def __init__(self, hostname="localhost", address="test_queue", count=1, message=None, body=None):
        # prefetch is set to zero so that proton does not automatically issue 10 credits.
        super(SimpleSenderHandler, self).__init__()
        self.hostname = hostname
        self.conn = None
        self.address = address
        self.error = False
        self.counter = 0
        self.max_messages = count
        self.sender = None
        self.body = body
        self.message = message

    def on_start(self, event):
        self.conn = event.container.connect(self.hostname)
        self.sender = event.container.create_sender(self.conn)

    def on_sendable(self, event):
        if event.sender:
            if self.counter < self.max_messages:
                if self.message is None:
                    msg = Message(address=self.address, body=self.body,
                                  properties={'seq': self.counter})
                else:
                    msg = self.message
                event.sender.send(msg)
                self.sender.msg_cnt += 1
        if self.counter == self.max_messages:
            self.conn.close()

    def on_connection_closed(self, event):
        event.container.stop()

    def run(self):
        Container(self).run()
