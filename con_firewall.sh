#!/bin/bash



# Define the l3config file path

L3CONFIG="l3config"

L2CONFIG="l2config"



# Write the l3config rules

echo '[

  {

    "priority": 1,

    "src_ip": "192.168.2.10",

    "dst_ip": "192.168.2.30",

    "nw_proto": "icmp",

    "action": "deny"

  },

  {

    "priority": 2,

    "src_ip": "192.168.2.20",

    "dst_ip": "192.168.2.40",

    "nw_proto": "icmp",

    "action": "deny"

  },

  {

    "priority": 3,

    "src_ip": "192.168.2.20",

    "dst_ip": "any",

    "nw_proto": "tcp",

    "dst_port": 80,

    "action": "deny"

  },

  {

    "priority": 4,

    "src_ip": "192.168.2.10",

    "dst_ip": "192.168.2.20",

    "nw_proto": "tcp",

    "action": "deny"

  },

  {

    "priority": 5,

    "src_ip": "192.168.2.10",

    "dst_ip": "192.168.2.20",

    "nw_proto": "udp",

    "action": "deny"

  }

]' > $L3CONFIG



# Write the l2config rule

echo '[

  {

    "priority": 6,

    "src_mac": "00:00:00:00:00:02",

    "dst_mac": "00:00:00:00:00:04",

    "action": "deny"

  }

]' > $L2CONFIG



echo "Configuration files have been updated."



# Apply the configuration rules (hypothetical command)

# replace `apply_rules_command` with the actual command to apply rules

# apply_rules_command --l3config $L3CONFIG --l2config $L2CONFIG

