# Imports
from pyroute2 import IPDB, WireGuard
from pyroute2 import NDB
# from tunfish.network.iptables import iptables


class Interface:

    def __init__(self):
        self.ifname = None
        self.ip = None

    def create(self, **kwargs):
        # Create WireGuard Interface
        self.ifname = kwargs.get('ifname')
        self.ip = kwargs.get('ip')

        with IPDB() as ip:
            dev = ip.create(kind='wireguard', ifname=self.ifname)
            dev.add_ip(self.ip)
            dev.up()
            dev.commit()

        wg = WireGuard()
        wg.set(self.ifname, private_key=kwargs.get('privatekey'), listen_port=kwargs.get('listenport'))

    # noch nicht getestet
    def delete(self, **kwargs):
        self.ifname = kwargs.get('ifname')
        with IPDB() as ip:
            dev = ip.delete(ifname=self.ifname)
            dev.commit()

    def addpeer(self, **kwargs):
        # Create WireGuard object
        wg = WireGuard()

        # build peer dict
        peer = {}
        for key in kwargs.keys():
            if key == 'publickey':
                peer = {**peer, **{'public_key': kwargs.get('publickey')}}
            if key == 'endpointaddr':
                peer = {**peer, **{'endpoint_addr': kwargs.get('endpointaddr')}}
            if key == 'endpointport':
                peer = {**peer, **{'endpoint_port': kwargs.get('endpointport')}}
            if key == 'keepalive':
                peer = {**peer, **{'persistent_keepalive': kwargs.get('keepalive')}}
            if key == 'allowedips':
                peer = {**peer, **{'allowed_ips': kwargs.get('allowedips')}}

        print(f"peer: {peer}")

        # add peer
        wg.set(self.ifname, peer=peer)

    def removepeer(self):
        pass

