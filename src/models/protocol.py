class Protocol(object):
    def __init__(self, default_port=None):
        self.name = type(self).__name__
        self.default_port = default_port


class Amqp(Protocol):
    def __init__(self, default_port=5672):
        super(Amqp, self).__init__(default_port)
        self.name = "AMQP 1.0"


class Mqtt(Protocol):
    def __init__(self, default_port=5672):
        super(Mqtt, self).__init__(default_port)


class Openwire(Protocol):
    def __init__(self, default_port=5672):
        super(Openwire, self).__init__(default_port)


class Stomp(Protocol):
    def __init__(self, default_port=5672):
        super(Stomp, self).__init__(default_port)
