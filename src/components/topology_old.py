class Topology(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is not None:
            return cls.instance
        else:
            cls.instance = super(Topology, cls).__new__(args, kwargs)
            return cls.instance

    def __init__(self, in_node=None, out_node=None):
        self.in_node = in_node
        self.out_node = out_node

# class Topology(object):
#    def __init__(self, configuration=None):
#        self.routers = []
#        self.brokers = []
#        self.connections = []
#        self.facades = []
#        self.configuration = configuration
#
#    def apply(self):
#        raise NotImplemented
#
#    def deactivate(self):
#        raise NotImplemented
#
#    @classmethod
#    def get_usable_topologies(cls):
#        raise NotImplemented
#
#    def __get_random(self, target=[]):
#        return random.randrange(start=0, stop=len(target))
#
#    def get_random_router(self):
#        return self.__get_random(self.routers)
#
#    def get_random_broker(self):
#        return self.__get_random(self.brokers)
#
#    def get_random_connection(self):
#        return self.__get_random(self.connections)
