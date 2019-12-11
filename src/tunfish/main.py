import sys

VERSION = '0.1.0'


def show_version():
    print(f"Version: {VERSION}")


def start_server():
    # from server.server import MyServer
    # server = MyServer()
    from tunfish.server import PortierServer
    server = PortierServer()
    server.start()


def start_client():
    name = sys.argv[1]
    from tunfish.client import TunfishClient
    client = TunfishClient()
    client.start(name)


def start_gateway():
    name = sys.argv[1]
    from tunfish.gateway import TunfishGateway
    gateway = TunfishGateway()
    gateway.start(name)
