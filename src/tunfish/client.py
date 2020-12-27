from os import environ
import time

import asyncio
from functools import partial

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

import iptc

import json

# PATH = '/vagrant/config/'
PATH = '/vagrant/etc/tunfish/'
CERTPATH = '/vagrant/certs/'


class Component(ApplicationSession):

    data = None

    async def onJoin(self, details):

        def got(started, msg, ff):
            print(f"result received")
            res = ff.result()
            duration = 1000. * (time.process_time() - started)
            print("{}: {} in {}".format(msg, res, duration))
            if msg == "REQUEST GATEWAY":
                # TODO: open interface
                from tunfish.model import Router
                router = Router()

                # new interface/wg control
                print(f"new control")
                router.interface.create(ifname=self.data['device_id'], ip=self.data['ip']+"/"+self.data['mask'], privatekey=self.data['wgprvkey'], listenport=42001)
                router.interface.addpeer(ifname=self.data['device_id'], publickey=res['wgpubkey'], endpointaddr=res['endpoint'], endpointport=res['listen_port'], keepalive=10, allowedips={'0.0.0.0/0'})

                # set rule
                # router.dev.rule('del', table=10, src='192.168.100.10/24')
                # router.dev.rule('add', table=10, src='172.16.100.15/16')
                # router.dev.rule('add', table=10, src='10.0.23.15/16')
                router.dev.rule('add', table=10, src=self.data['ip']+"/"+self.data['mask'])
                # set route
                # router.dev.route('del', table=10, src='192.168.100.10/24', oif=idx)
                idx = router.dev.link_lookup(ifname=self.data['device_id'])[0]
                router.dev.route('add', table=10, src='10.0.42.15/16', gateway='10.0.23.15', oif=idx)

                # iptables
                chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "POSTROUTING")
                rule = iptc.Rule()
                rule.out_interface = "tf-0815"
                target = iptc.Target(rule, "MASQUERADE")
                rule.target = target
                chain.insert_rule(rule)

        with open(PATH + self.config.extra['v1'] + '.json', 'r') as f:
            self.data = json.load(f)
        print(f"self.data: {self.data}")
        t1 = time.process_time()

        # task = self.call(u'com.portier.requestgateway', self.data, options=CallOptions(timeout=0))
        task = self.call(u'com.portier.request_gateway', self.data)
        task.add_done_callback(partial(got, t1, "REQUEST GATEWAY"))
        await asyncio.gather(task)

        t1 = time.process_time()
        task = self.call(u'com.portier.request_status')
        task.add_done_callback(partial(got, t1, "REQUEST STATUS"))
        await asyncio.gather(task)

        print(f"EXTRA: {self.config.extra['v1']}")

        self.leave()

    def onDisconnect(self):
        # delete interface
        # reconnect
        asyncio.get_event_loop().stop()


class TunfishClient:

    clientdata = None

    def start(self, conf):

        import six
        import ssl

        with open(PATH + conf + '.json', 'r') as f:
            self.clientdata = json.load(f)

        cf = CERTPATH + self.clientdata['cf']
        kf = CERTPATH + self.clientdata['kf']
        caf = CERTPATH + self.clientdata['caf']

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
        runner = ApplicationRunner(url, realm, ssl=client_ctx, extra={'v1': conf})
        runner.run(Component)




