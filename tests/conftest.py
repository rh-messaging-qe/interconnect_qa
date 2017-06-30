import pytest

from src.components.topology import Topology

def pytest_addoption(parser):
    parser.addoption("--in_node", action="store", default="localhost", help="node for ingress connection")
    parser.addoption("--out_node", action="store", default="localhost", help="node for egress connection")
    parser.addoption("--sender_node", action="store", default="localhost", help="node where sender is running")
    parser.addoption("--receiver_node", action="store", default="localhost", help="node where receiver is running")

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
