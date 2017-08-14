from src.models.protocols import Amqp, Mqtt, Stomp
from src.models.node import Node


class Client(object):
    """

    """
    supported_protocols = None

    def __init__(self):
        self.logs = None  # @TODO

    class Sender(object):
        def __init__(self):
            pass

    class Receiver(object):
        def __init__(self,):
            pass


class NativeClient(object, Client):
    def __init__(self):
        pass


class ExternalClient(object, Client):
    def __init__(self, node: Node):
        self.node = node


class Proton(NativeClient):
    """

    """
    supported_protocols = [Amqp()]

    def __init__(self, node):
        super(Proton, self).__init__(node)
