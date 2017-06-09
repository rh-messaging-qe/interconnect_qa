import pytest

from src.components.topology import Topology


#@pytest.fixture(scope="module", params=Topology.get_usable_topologies())
#def topology(request):
#    topology = Topology(request.param)
#    topology.apply()
#    yield topology
#    topology.deactivate()
#
#@pytest.fixture(scope="function")
#def facades(topology):
#    return topology.facades

@pytest.fixture(scope="module", autouse=True)
def in_node():
    return Topology.instance.in_node

@pytest.fixture(scope="module", autouse=True)
def out_node():
    return Topology.instance.out_node

@pytest.fixture(scope="module", autouse=True)
def sender_node():
    return Topology.instance.sender_node

@pytest.fixture(scope="module", autouse=True)
def receiver_node():
    return Topology.instance.receiver_node

def test_send_receive(in_node, out_node, sender_node, receiver_node):
    sender_node.send(in_node)
    receiver_node.receive(out_node)
    assert sender_node.last_message == receiver_node.last_message

#def test_send_facade_receive_facade_router_only(topology, facades):
#    client.
#    for facade in facades:
#        address = facade.hostname
#        for connection in facade.ongoing:
#            connection.send(address=address)
#            connection.receive(address=address)
#            assert connection.last_sent == connection.last_received


#def test_send_facade_receive_router_random(topology):
#    address = topology.get_facade().hostname
#    for connection in topology.connections:
#        address_for_receiver = topology.get_random_router().hostname
#        connection.send(address=address)
#        connection.receive(address=address_for_receiver)
#        assert connection.last_sent == connection.last_received
#
#
#def test_send_router_random_receive_facade(topology):
#    address = topology.get_facade().hostname
#    for client in clients:
#        address_for_sender = topology.get_random_router().hostname
#        client.send(address=address_for_sender)
#        client.receive(address=address)
#        assert client.last_sent == client.last_received
#
#
#def test_send_router_random_receive_router_random(topology):
#    for client in clients:
#        address_for_sender = routers.get_random_router().hostname
#        address_for_receiver = routers.get_random_router().hostname
#        client.send(address=address_for_sender)
#        client.receive(address=address_for_receiver)
#        assert client.last_sent == client.last_received
