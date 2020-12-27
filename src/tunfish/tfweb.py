from os import environ
import asyncio
from functools import partial
import time
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def onJoin(self, details):

        def on_event(i):
            print("Got event: {}".format(i))
            # self.received += 1
            # if self.received > 5:
            #     self.leave()

        await self.subscribe(on_event, 'com.topic.portier.status')


class TunfishWeb:
    def start(self):
        import six
        import ssl

        cf = '/vagrant/certs/tf-web.pem'
        kf = '/vagrant/certs/tf-web.key'
        caf = '/vagrant/certs/ca.pem'

        tfweb_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        tfweb_ctx.verify_mode = ssl.CERT_REQUIRED
        tfweb_ctx.options |= ssl.OP_SINGLE_ECDH_USE
        tfweb_ctx.options |= ssl.OP_NO_COMPRESSION
        tfweb_ctx.load_cert_chain(certfile=cf, keyfile=kf)
        tfweb_ctx.load_verify_locations(cafile=caf)
        tfweb_ctx.set_ciphers('ECDH+AESGCM')

        # url = environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://127.0.0.1:8080/ws")
        # url = environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://172.16.42.2:8080/ws")
        url = environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://172.16.42.2:8080/ws")
        print(f"URL: {url}")
        if six.PY2 and type(url) == six.binary_type:
            url = url.decode('utf8')
        realm = u"tf_cb_router"
        # runner = ApplicationRunner(url, realm, ssl=tfweb_ctx)
        runner = ApplicationRunner(u"ws://172.16.42.2:9000/ws", realm)
        runner.run(Component)
