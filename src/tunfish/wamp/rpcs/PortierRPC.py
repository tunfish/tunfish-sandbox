from sqlalchemy import exc
from tunfish.model import Network
from tunfish.model import Gateway
from tunfish.model import Router
from tunfish.database.control import dbc


class ServerRPC:

    def __init__(self, fabric):
        self.dbc_handler = dbc()
        self.fabric = fabric

    # data json dict
    async def request_gateway(self, data):
        print(f"data: {data}")
        print(f"query gateway")
        gateway = self.dbc_handler.session.query(Gateway).filter_by(active=True).order_by(Gateway.counter).first()
        print(f"Gateway: {gateway}")
        print(f"done.")
        pubkey = await self.fabric.call(u'com.gw.open_interface', data)

        print(f"value task: {pubkey}")

        gw = {
            "ip": gateway.ip,
            "name": gateway.name,
            "wgpubkey": pubkey,
            "listen_port": 42001,
            "endpoint": gateway.ip
        }
        # maybe better way, not tested
        # return gateway.__dict__
        return gw

    def register_gateway(self, data):
        print(f"register_gateway_data: {data}")
        gateway = self.dbc_handler.session.query(Gateway).filter_by(name=data['name']).first()
        print(f"GATEWAY: {gateway}")
        gateway.active = True
        self.dbc_handler.session.commit()

    def request_status(self):
        print(f"Status: {self.__dict__}")

    def add_network(self, data):
        print(f"received data from tf-ctl: {data}")
        network = Network(**data)
        print(f"NETWORK: {network}")
        try:
            self.dbc_handler.session.add(network)
            self.dbc_handler.session.commit()
        except exc.SQLAlchemyError as e:
            print(f"Error: {e}")
            self.dbc_handler.session.rollback()
        except Exception as e:
            print(f"{e}")

    def add_gateway(self, data):
        print(f"received data from tf-ctl: {data}")
        network = self.dbc_handler.session.query(Network).filter_by(name=data['network']).first()
        network.gateway.append(Gateway(**data))
        print(f"NETWORK_QUERY:{network.__dict__}")

        try:
            self.dbc_handler.session.add(network)
            self.dbc_handler.session.commit()
        except exc.SQLAlchemyError as e:
            print(f"Error: {e}")
            self.dbc_handler.session.rollback()
        except Exception as e:
            print(f"{e}")

        from tunfish.tools.certificate import Certificate
        cert = Certificate()
        cert.gen_x509(name=data['name'])

    def add_client(self, data):
        print(f"received data from tf-ctl: {data}")
        network = self.dbc_handler.session.query(Network).filter_by(name=data['network']).first()
        network.router.append(Router(**data))
        print(f"NETWORK_QUERY:{network.__dict__}")
        try:
            self.dbc_handler.session.add(network)
            self.dbc_handler.session.commit()
        except exc.SQLAlchemyError as e:
            print(f"Error: {e}")
            self.dbc_handler.session.rollback()
        except Exception as e:
            print(f"{e}")

    def web_get_networks(self):
        network = self.dbc_handler.session.query(Network.name).all()

        print(f"network {network}")

        return network
