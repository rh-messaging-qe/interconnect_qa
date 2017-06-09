from src.tools.receiver import SimpleReceiverHandler
from src.tools.sender import SimpleSenderHandler


class Node(object):
    def __init__(self, hostname):
        self.hostname = hostname


class ClientNode(Node):
    def __init__(self, hostname, client=None):
        super(ClientNode, self).__init__(hostname)
        self.client = client

    @property
    def last_message(self):
        return self.client.message_pool[-1]

class BasicSenderNode(ClientNode):
    def __init__(self, hostname, sender=SimpleSenderHandler):
        super(BasicSenderNode, self).__init__(hostname, sender())

    def send(self, node, address=None, count=1, message=None):
        self.client.hostname = node.hostname
        self.client.address = address or self.client.address  # use default value if given is None
        self.client.count = count
        self.client.message = message or self.client.message
        self.client.run()


class BasicReceiverNode(ClientNode):
    def __init__(self, hostname, receiver=SimpleReceiverHandler):
        super(BasicReceiverNode, self).__init__(hostname, receiver())

    def receive(self, node, address=None, count=1):
        self.client.hostname = node.hostname
        self.client.address = address or self.client.address  # use default value if given is None
        self.client.count = count
        self.client.run()
