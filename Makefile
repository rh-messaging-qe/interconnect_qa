% Makefile
all: unit-test-topology

unit-test-topology:
	cd selftests/tool_tests/ && \
	pytest test_topology.py
