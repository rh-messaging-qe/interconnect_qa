import pytest

from src.components.topology import Topology


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
