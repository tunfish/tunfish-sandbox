from os import environ
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from tunfish.model import Gateway
from tunfish.database.control import dbc


class Component(ApplicationSession):
    dbc_handler = dbc()

    async def onJoin(self, details):
        # data json dict
        async def RequestGateway(data):
            print(f"data: {data}")
            gateway = self.dbc_handler.session.query(Gateway).filter_by(active=True).order_by(Gateway.counter).first()

            pubkey = await self.call(u'com.gw.openinterface', data)
            print(f"value task: {pubkey}")

            gw = {
                "ip": gateway.ip,
                "name": gateway.name,
                "wgpubkey": pubkey,
                "listen_port": 42001,
                "endpoint": "192.168.100.10"
            }
            return gw

        await self.register(RequestGateway, u'com.portier.requestgateway')
        print("Registered com.portier.requestgateway")

        def register_gateway(data):
            gateway = self.dbc_handler.session.query(Gateway).filter_by(name=data['name']).first()
            print(f"GATEWAY: {gateway}")
            gateway.active = True
            self.dbc_handler.session.commit()

        await self.register(register_gateway, u'com.portier.registergateway')
        print("Registered com.portier.registergateway")

        print(f"DETAILS: {details}")

        def requestStatus():
            print(f"Status: {self.__dict__}")

        await self.register(requestStatus, u'com.portier.requeststatus')


class PortierServer:
    def start(self):
        import six
        import ssl
        # TLS
        # Setup server

        cf = '/vagrant/certs/server.pem'
        kf = '/vagrant/certs/server.key'
        caf = '/vagrant/certs/ca.pem'

        server_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        server_ctx.verify_mode = ssl.CERT_REQUIRED
        server_ctx.options |= ssl.OP_SINGLE_ECDH_USE
        server_ctx.options |= ssl.OP_NO_COMPRESSION
        server_ctx.load_cert_chain(certfile=cf, keyfile=kf)
        server_ctx.load_verify_locations(cafile=caf)
        server_ctx.set_ciphers('ECDH+AESGCM')

        # url = environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://127.0.0.1:8080/ws")
        url = environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://192.168.42.1:8080/ws")
        print(f"URL: {url}")
        if six.PY2 and type(url) == six.binary_type:
            url = url.decode('utf8')
        realm = u"tf_cb_router"
        runner = ApplicationRunner(url, realm, ssl=server_ctx)
        runner.run(Component)
