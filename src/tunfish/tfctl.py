from os import environ
import time
import asyncio
from functools import partial
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
import json
import argparse

PATH = '/vagrant/etc/tunfish/'
CERTPATH = '/vagrant/certs/'


class Component(ApplicationSession):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None

    async def onJoin(self, details):

        def got(started, msg, ff):
            res = ff.result()
            duration = 1000. * (time.process_time() - started)
            print("{}: {} in {}".format(msg, res, duration))

            if msg == "ADD NETWORK":
                print(f"Network added... done.")

            if msg == "ADD GATEWAY":
                print(f"Gateway added... done.")

            if msg == "ADD CLIENT":
                print(f"Client added... done.")

        print(f"extra: {self.config.extra['v1']}")
        args = json.loads(self.config.extra['v1'])

        if args['addNetwork'] is not None:
            print(f"self.data.addNetwork: {args['addNetwork']}")
            d = {}
            for i in args['addNetwork']:
                k = i.split('=', 1)[0]
                v = i.split('=', 1)[1]
                d[k] = v
            print(f"DICT: {d}")

            t1 = time.process_time()
            task = self.call(u'com.portier.add_network', d)
            task.add_done_callback(partial(got, t1, "ADD NETWORK"))
            await asyncio.gather(task)

        if args['addGW'] is not None:
            print(f"self.data.addGW: {args['addGW']}")
            d = {}
            for i in args['addGW']:
                k = i.split('=', 1)[0]
                v = i.split('=', 1)[1]
                d[k] = v
            print(f"DICT: {d}")

            t1 = time.process_time()
            task = self.call(u'com.portier.add_gateway', d)
            task.add_done_callback(partial(got, t1, "ADD GATEWAY"))
            await asyncio.gather(task)

        if args['addClient'] is not None:
            print(f"self.data.addClient: {args['addClient']}")
            d = {}
            for i in args['addClient']:
                k = i.split('=', 1)[0]
                v = i.split('=', 1)[1]
                d[k] = v
            print(f"DICT: {d}")
            t1 = time.process_time()
            task = self.call(u'com.portier.add_client', d)
            task.add_done_callback(partial(got, t1, "ADD CLIENT"))
            await asyncio.gather(task)

        self.leave()

    def onDisconnect(self):
        # delete interface
        # reconnect
        asyncio.get_event_loop().stop()


class TunfishControl:

    controldata = None

    def tf_parse(self, clargs):

        parser = argparse.ArgumentParser()
        parser.add_argument("--addNetwork",
                            metavar="KEY=VALUE",
                            nargs="+",
                            help="add new network"
                                 "name=unique name for the network (required)"
                                 "(not yet implemented) services=service1,service2,... \
                                 which service should be available at the network ")

        parser.add_argument("--addGW",
                            metavar="KEY=VALUE",
                            nargs="+",
                            help="add new gateway"
                                 "name=unique name for the gateway (required)"
                                 "ip=publicIP (required)"
                                 "network=network to which the gateway should be added")

        parser.add_argument("--addClient",
                            metavar="KEY=VALUE",
                            nargs="+",
                            help="add new client"
                                 "name=unique name for the client (required)"
                                 "network=network to which the client should be added (required)")

        print(f"1")
        args = parser.parse_args(args=clargs[1:])
        print(f"2")
        # if args.addGW:
        #     print(f"add Gateway... {args}")
        #     return args.addGW
        print(f"ARGS: {args}")
        print(f"ARGS.__dict__: {args.__dict__}")
        return json.dumps(args.__dict__)

    def start(self, conf):

        print(f"ARGS: {conf}")
        data = self.tf_parse(conf)
        import six
        import ssl

        with open(PATH + 'tf-ctl' + '.json', 'r') as f:
            self.controldata = json.load(f)

        cf = CERTPATH + self.controldata['cf']
        kf = CERTPATH + self.controldata['kf']
        caf = CERTPATH + self.controldata['caf']

        client_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        client_ctx.verify_mode = ssl.CERT_REQUIRED
        client_ctx.options |= ssl.OP_SINGLE_ECDH_USE
        client_ctx.options |= ssl.OP_NO_COMPRESSION
        client_ctx.load_cert_chain(certfile=cf, keyfile=kf)
        client_ctx.load_verify_locations(cafile=caf)
        client_ctx.set_ciphers('ECDH+AESGCM')

        # url = environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://127.0.0.1:8080/ws")
        url = environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://172.16.42.2:8080/ws")
        print(f"URL: {url}")
        if six.PY2 and type(url) == six.binary_type:
            url = url.decode('utf8')
        realm = u"tf_cb_router"
        runner = ApplicationRunner(url, realm, ssl=client_ctx, extra={'v1': data})
        runner.run(Component)
