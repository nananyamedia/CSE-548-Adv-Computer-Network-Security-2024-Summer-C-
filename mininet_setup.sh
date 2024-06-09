#!/bin/bash

# Ensure mininet is installed
if ! command -v mn &> /dev/null
then
    echo "Mininet could not be found. Please install it first."
    exit
fi

# Run the custom topology Python script
sudo mn --custom mininet_topology.py --topo mytopo --controller remote
