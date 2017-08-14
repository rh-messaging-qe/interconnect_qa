class Node(object):
    """
    Represents virtual destination/service aka node.
    In a case of interconnect vm with qdrouterd is represented as a Router node.
    When there is a sender present on such node, it is a Sender node.
    All future representations should inherit from this class.
    """

    # TODO: restart method
    def __init__(self, hostname="localhost", ):
        self.hostname = hostname

