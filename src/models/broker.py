from src.components.models.protocol import Amqp, Mqtt, Stomp, Openwire
from src.components.node import Node


class Broker(object):
    """

    """
    supported_protocols = None

    def __init__(self, node: Node):
        self.node = node
        self.logs = None  # @TODO


class Artemis(Broker):
    """

    """
    supported_protocols = [Amqp(), Mqtt(), Stomp(), Openwire()]

    def __init__(self, node):
        super(Artemis, self).__init__(node)


class Qpid(Broker):
    """

    """
    supported_protocols = [Amqp()]

    def __init__(self, node):
        super(Qpid, self).__init__(node)
