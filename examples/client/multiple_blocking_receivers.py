# !/usr/bin/python

import threading
from uuid import uuid4

from proton.utils import BlockingConnection

ROUTER_ADDRESS = "proton+amqp://mlesko-236x.usersys.redhat.com:5672"
# ROUTER_ADDRESS = "proton+amqp://mlesko-246x.usersys.redhat.com:5672"
ADDRESS = "pulp.address"
HEARTBEAT = 60
# SLEEP_MIN = 1.9
# SLEEP_MAX = 2.1
THREADS = 100
RECEIVERS = 100


class ReceiverThread(threading.Thread):
    def __init__(self, _id, address=ADDRESS, domain=None):
        super(ReceiverThread, self).__init__()
        self._id = _id
        self.address = address
        self.domain = domain
        self.running = True
        self.nr = 0
        self.max = RECEIVERS

    def connect(self):
        self.conn = BlockingConnection(ROUTER_ADDRESS, ssl_domain=self.domain, heartbeat=HEARTBEAT)

    def run(self):
        self.connect()
        for x in xrange(self.max):
            name = '%s.%s' % (self.address, x)
            self.recv = self.conn.create_receiver(name, name=str(uuid4()), dynamic=False,
                                                  options=None)
            print("created: ", name)


threads = []

for i in range(THREADS):
    threads.append(ReceiverThread(i, '%s.%s' % (ADDRESS, i)))
    threads[i].start()

for i in range(THREADS):
    threads[i].join()
