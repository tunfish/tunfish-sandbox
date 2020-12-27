from os import environ
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
import json
from tunfish.model import Router
from tunfish.model import Gateway
from tunfish.wamp.rpcs.GatewayRPC import GatewayRPC



# PATH = '/vagrant/config/'
PATH = '/vagrant/etc/tunfish/'
CERTPATH = '/vagrant/certs/'


class Component(ApplicationSession):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gw_procedures = GatewayRPC(self)

    async def onJoin(self, details):

        # TODO: make code generic
        # - read config for specific gateway
        # - data structure for opened interfaces
        # - ...

        with open(PATH + self.config.extra['v1'] + '.json', 'r') as f:
            config = json.load(f)

        print(f"CONFIG: {config}")

        try:
            self.call(u'com.portier.register_gateway', config)
        except Exception as e:
            print(f"ERROR: can't register gateway {config['name']}, {e}")
            self.leave()

        # data json dict

        await self.register(self.gw_procedures.open_interface, u'com.gw.open_interface')
        print("Registered com.gw.open_interface")

        await self.register(self.gw_procedures.close_interface, u'com.gw.close_interface')
        print("Registered com.gw.close_interface")


class TunfishGateway:

    def start(self, conf):

        import six
        import ssl
        print(f"WHOIS: {PATH + conf}.json")
        with open(PATH + conf + '.json', 'r') as f:
            clientdata = json.load(f)

        cf = CERTPATH + clientdata['cf']
        kf = CERTPATH + clientdata['kf']
        caf = CERTPATH + clientdata['caf']

        gateway_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        gateway_ctx.verify_mode = ssl.CERT_REQUIRED
        gateway_ctx.options |= ssl.OP_SINGLE_ECDH_USE
        gateway_ctx.options |= ssl.OP_NO_COMPRESSION
        gateway_ctx.load_cert_chain(certfile=cf, keyfile=kf)
        gateway_ctx.load_verify_locations(cafile=caf)
        gateway_ctx.set_ciphers('ECDH+AESGCM')

        # url = environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://127.0.0.1:8080/ws")
        url = environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://172.16.42.2:8080/ws")
        print(f"URL: {url}")
        if six.PY2 and type(url) == six.binary_type:
            url = url.decode('utf8')
        realm = u"tf_cb_router"
        runner = ApplicationRunner(url, realm, ssl=gateway_ctx, extra={'v1': conf})
        runner.run(Component)
