import sys

VERSION = '0.1.0'


def show_options():
    print(f"--help      show help")
    print(f"--version   show version")
    print(f" ")
    print(f"--server    start as server")
    print(f"--gateway   start as gateway")
    print(f"--client    start as client")


def show_version():
    print(f"Version: {VERSION}")


def start_server():
    # from server.server import MyServer
    # server = MyServer()
    from tunfish.server import PortierServer
    server = PortierServer()
    server.start()


def start_client(name):
    from tunfish.client import TunfishClient
    client = TunfishClient()
    client.start(name)


def start_gateway(name):
    from tunfish.gateway import TunfishGateway
    gateway = TunfishGateway()
    gateway.start(name)


def main():
    for arg in sys.argv[1:]:
        if arg == '--server':
            start_server()
        elif arg == '--client':
            start_client(sys.argv[2])
        elif arg == '--gateway':
            start_gateway(sys.argv[2])
        elif arg == '--help':
            show_options()
        elif arg == '--version':
            show_version()
        else:
            show_options()


if __name__ == '__main__':
    main()
