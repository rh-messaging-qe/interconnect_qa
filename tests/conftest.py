import pytest

from src.components.node import BasicSenderNode, BasicReceiverNode
from src.components.router import Router


def pytest_addoption(parser):
    parser.addoption("--in_node", action="store", default="localhost", help="node for ingress connection")
    parser.addoption("--out_node", action="store", default="localhost", help="node for egress connection")
    parser.addoption("--sender_node", action="store", default="localhost", help="node where sender is running")
    parser.addoption("--receiver_node", action="store", default="localhost", help="node where receiver is running")


@pytest.fixture(scope="module", autouse=True)
def in_node(request):
    return Router(request.config.getoption("in_node"))


@pytest.fixture(scope="module", autouse=True)
def out_node(request):
    return Router(request.config.getoption("out_node"))


@pytest.fixture(scope="module", autouse=True)
def sender_node(request):
    return BasicSenderNode(request.config.getoption("sender_node"))


@pytest.fixture(scope="module", autouse=True)
def receiver_node(request):
    return BasicReceiverNode(request.config.getoption("receiver_node"))
