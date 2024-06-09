#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, Host
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def myNetwork():
    net = Mininet(topo=None, build=False, ipBase='192.168.2.0/24')

    info('*** Adding controller\n')
    c1 = net.addController(name='c1', controller=RemoteController, ip='127.0.0.1', port=6633)
    c2 = net.addController(name='c2', controller=RemoteController, ip='127.0.0.1', port=6634)

    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, dpid='0000000000000001')

    info('*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='192.168.2.10', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='192.168.2.20', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='192.168.2.30', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='192.168.2.40', defaultRoute=None)

    info('*** Add links\n')
    net.addLink(c1, s1)
    net.addLink(c2, s1)
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    net.addLink(s1, h4)

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s1').start([c1, c2])

    info('*** Applying flow rules\n')
    applyFlowRules(net)

    CLI(net)
    net.stop()

def applyFlowRules(net):
    s1 = net.get('s1')
    s1.dpctl('del-flows')

    # Allow basic connectivity (ARP, etc.)
    s1.dpctl('add-flow', 'priority=10,arp,actions=normal')
    s1.dpctl('add-flow', 'priority=10,ip,actions=normal')

    # Block ICMP traffic from 192.168.2.10 to 192.168.2.30
    s1.dpctl('add-flow', 'priority=100,ip,nw_src=192.168.2.10,nw_dst=192.168.2.30,icmp,actions=drop')

    # Block ICMP traffic from 192.168.2.20 to 192.168.2.40
    s1.dpctl('add-flow', 'priority=100,ip,nw_src=192.168.2.20,nw_dst=192.168.2.40,icmp,actions=drop')

    # Block HTTP traffic from 192.168.2.20
    s1.dpctl('add-flow', 'priority=100,ip,nw_src=192.168.2.20,tp_dst=80,actions=drop')

    # Block TCP traffic from 192.168.2.10 to 192.168.2.20
    s1.dpctl('add-flow', 'priority=100,ip,nw_src=192.168.2.10,nw_dst=192.168.2.20,tcp,actions=drop')

    # Block UDP traffic from 192.168.2.10 to 192.168.2.20
    s1.dpctl('add-flow', 'priority=100,ip,nw_src=192.168.2.10,nw_dst=192.168.2.20,udp,actions=drop')

    # Block traffic from MAC address 00:00:00:00:00:02 to 00:00:00:00:00:04
    s1.dpctl('add-flow', 'priority=100,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:04,actions=drop')

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
