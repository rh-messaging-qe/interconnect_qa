from src.components.client import Sender, Receiver
from src.tools.receiver import SimpleReceiverHandler
from src.tools.sender import SimpleSenderHandler


class Node(object):
    def __init__(self, hostname="localhost"):
        self.hostname = hostname


class ClientNode(Node):
    def __init__(self, hostname, client=None):
        super(ClientNode, self).__init__(hostname)
        self.client_class = client
        self.client = None

    @property
    def last_message(self):
        return self.client.message_pool[-1]

class BasicSenderNode(ClientNode):
    def __init__(self, hostname, sender=Sender):
        super(BasicSenderNode, self).__init__(hostname, sender)

    def send(self, node, address=None, count=1, messages=[]):
        self.client = self.client_class(hostname=node.hostname, address=address, count=count, messages=messages)
        self.client.run()


class BasicReceiverNode(ClientNode):
    def __init__(self, hostname, receiver=Receiver):
        super(BasicReceiverNode, self).__init__(hostname, receiver)

    def receive(self, node, address=None, expected=1):
        self.client = self.client_class(hostname=node.hostname, address=address, expected=expected)
        self.client.run()
