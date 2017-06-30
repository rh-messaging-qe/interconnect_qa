from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

import threading


class Timeout(object):
    def __init__(self, handler):
        self.registrated_handler = handler

    def on_timer_task(self, event):
        self.registrated_handler.timeout(event)


class Client(MessagingHandler):
    def __init__(self, blocking=False):
        super(Client, self).__init__()
        self.hostname = None
        self.address = None
        self.message_pool = []
        self.error = False
        self.container = None
        self.event = None
        self.thread = None
        self._blocking = blocking

    @property
    def msg_cnt(self):
        return len(self.message_pool)

    def run(self):
        self.thread = threading.Thread(target=self.container.run)
        if self._blocking:
            self.thread.run()
        else:
            self.thread.start()

    def stop(self):
        self.thread.join(timeout=1)


class Sender(Client):
    def __init__(self, hostname="localhost", address="test_queue", count=1, messages=[], blocking=False):
        super(Sender, self).__init__(blocking=blocking)
        self.hostname = hostname
        self.address = address
        self.counter = 0
        self.max_messages = count
        self.messages = messages
        self.container = None
        self.container = Container(self)

    def on_start(self, event):
        conn = event.container.connect(self.hostname)
        event.container.create_sender(conn, self.address)

    def on_sendable(self, event):
        if event.sender:
            for message in self.messages:
                counter_per_message = 0
                if counter_per_message < self.max_messages:
                    event.sender.send(message)
                    self.message_pool.append(message)
                    counter_per_message += 1
                self.counter += 1
            if self.counter == self.max_messages:
                event.connection.close()

    def on_connection_closed(self, event):
        event.container.stop()


class Receiver(Client):
    def __init__(self, hostname="localhost", address="test_queue", expected=1, blocking=True):
        super(Receiver, self).__init__(blocking=blocking)
        self.hostname = hostname
        self.confirmed = 0
        self.total = expected
        self.received = 0
        self.receiver = None
        self.address = address
        self.container = Container(self)

    def on_reactor_init(self, event):
        super(Receiver, self).on_reactor_init(event)
        self.timer = event.reactor.schedule(5, Timeout(self))
        self.receiver = event.container.create_receiver(self.hostname + "/" + self.address)
        self.receiver.open()

    def timeout(self, event):
        self.error = 1
        if self.receiver is not None:
            self.receiver.close()
        event.container.stop()

    def on_message(self, event):
        if event.receiver:
            self.message_pool.append(event.message)
            self.received += 1
        if self.received == self.total:
            if self.receiver is not None:
                self.receiver.close()
        event.container.stop()
