class Connection(object):
    def __init__(self, sender=None, receiver=None, address="localhost", port=5672):
        self.sender = sender
        self.receiver = receiver
        self.address = address
        self.port = port

    def send(self, msg=None, cnt=1):
        self.sender.send(msg, cnt)

    def receive(self, msg=None, cnt=1):
        self.receiver.receive(msg, cnt)
