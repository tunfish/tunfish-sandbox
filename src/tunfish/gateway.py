from os import environ
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
import json
from tunfish.model import Router
import iptc

PATH = '/vagrant/config/'
CERTPATH = '/vagrant/certs/'


class Component(ApplicationSession):

    async def onJoin(self, details):

        # TODO: make code generic
        # - read config for specific gateway
        # - data structure for opened interfaces
        # - ...

        with open(PATH + self.config.extra['v1'] + '.json', 'r') as f:
            config = json.load(f)

        print(f"CONFIG: {config}")

        try:
            self.call(u'com.portier.registergateway', config)
        except Exception as e:
            print(f"ERROR: can't register gateway {config['name']}, {e}")
            self.leave()

        # data json dict
        def openInterface(data):
            print(f"data: {data}")

            # TODO: create wg keys
            # TODO: replace subprocess !!!
            # import subprocess

            # subprocess.call(f"wg genkey | tee privatekey+{data['device_id']} | wg pubkey > publickey+{data['device_id']}", shell=True)
            # with open(f"privatekey+{data['device_id']}", 'r') as f:
            #     priv = f.read()
            #     print(f"PRIV: {priv}")
            #     f.close()
            # with open(f"publickey+{data['device_id']}", 'r') as f:
            #     pub = f.read()
            #     print(f"PUB: {pub}")
            #     f.close()
            # subprocess.call(f"rm privatekey+{data['device_id']} && rm publickey+{data['device_id']}", shell=True)

            import pysodium
            from base64 import b64encode
            keys = pysodium.crypto_box_keypair()

            # TODO: open interface
            router = Router()
            router.device_id = data['device_id']
            print(f"{data}")

            router.dev.link('add', ifname=data['device_id'], kind='wireguard')
            idx = router.dev.link_lookup(ifname=data['device_id'])[0]
            print(f"IDX: {idx}")
            # router.dev.addr('add', index=idx, address='192.168.42.50', mask=24)
            router.dev.addr('add', index=idx, local='192.168.42.50', mask=32, address='192.168.100.10')
            print(f"setup config")

            # cfg = {
            #     "interface": data['device_id'] + POSTFIX,
            #     "listen_port": 42001,
            #     "private_key": priv,
            #     "peers": [{"public_key": data["wgpubkey"], "allowed_ips": ["0.0.0.0/0"]}]
            # }

            # router.wg.set_device(ifname=data['device_id'] + POSTFIX, config=cfg)
            # setup wireguard interface
            router.wg.set(interface=data['device_id'], private_key=b64encode(keys[0]), listen_port=42235)
            # add peer
            cfg = {'public_key': b64encode(data["wgpubkey"]), 'allowed_ips': ["0.0.0.0/0"]}
            router.wg.set(interface=data['device_id'], private_key=b64encode(keys[0]), peer=cfg)

            print(f"clientpubkey: {len(data['wgpubkey'])}")
            print(f"clientpubkey: {data['wgpubkey']}")

            router.dev.link('set', index=idx, state='up')

            # iptables for wg-interface
            chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
            rule = iptc.Rule()
            rule.out_interface = "tf_gateone"
            target = iptc.Target(rule, "ACCEPT")
            rule.target = target
            chain.insert_rule(rule)

            chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "POSTROUTING")
            rule = iptc.Rule()
            rule.out_interface = "eth0"
            target = iptc.Target(rule, "MASQUERADE")
            rule.target = target
            chain.insert_rule(rule)

            return b64encode(keys[0])

        await self.register(openInterface, u'com.gw.openinterface')
        print("Registered com.gw.openinterface")

        # com.gw.closeinterface
        # com.gw.status
        # com.gw....


class TunfishGateway:

    def start(self, conf):

        import six
        import ssl

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
        url = environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://192.168.42.1:8080/ws")
        print(f"URL: {url}")
        if six.PY2 and type(url) == six.binary_type:
            url = url.decode('utf8')
        realm = u"tf_cb_router"
        runner = ApplicationRunner(url, realm, ssl=gateway_ctx, extra={'v1': conf})
        runner.run(Component)
