from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, Date, Boolean
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from pyroute2 import IPRoute
from tunfish.network.interface import Interface


Base = declarative_base()


class Router(Base):

    __tablename__ = 'router'

    id = Column(Integer, Sequence('tf_id_seq'), primary_key=True)
    device_id = Column('device_id', String(32), unique=True, default=None)
    ip = Column('ip', String(32), default=None)
    device_pw = Column('device_pw', String(32), default=None)
    user_pw = Column('user_pw', String(32), default=None)
    wgprvkey = Column('wgprvkey', String(44), default=None)
    wgpubkey = Column('wgpubkey', String(44), default=None)
    doa = Column('doa', Date, default=None)
    dod = Column('dod', Date, default=None)
    hw_model = Column('hw_model', String(32), default=None)
    hw_version = Column('hw_version', String(32), default=None)
    sw_version = Column('sw_version', String(32), default=None)
    blocked = Column('blocked', Boolean, default=False)

    network_id = Column(Integer, ForeignKey('network.id'))
    network = relationship("Network", back_populates="router")

    gateway_id = Column(Integer, ForeignKey('gateway.id'))
    gateway = relationship("Gateway", back_populates="router")

    # config for wg interface
    listenport = Column('listenport', Integer, default=42001)
    endpoint = Column('endpoint', String(32), default=None)
    allowed_ips = Column('allowed_ips', String(32), default='0.0.0.0/0')

    def __init__(self, *args, **kwargs):

        self.device_id = kwargs.get('device_id')
        self.ip = kwargs.get('ip')
        self.device_pw = kwargs.get('device_pw')
        self.user_pw = kwargs.get('user_pw')
        self.wgprvkey = kwargs.get('wgprvkey')
        self.wgpubkey = kwargs.get('wgpubkey')
        self.doa = kwargs.get('doa')
        self.dod = kwargs.get('dod')
        self.hw_model = kwargs.get('hw_model')
        self.hw_version = kwargs.get('hw_version')
        self.sw_version = kwargs.get('sw_version')
        self.blocked = kwargs.get('blocked')
        self.gateway = kwargs.get('gateway')
        self.listenport = kwargs.get('listenport')
        self.endpoint = kwargs.get('endpoint')
        self.allowed_ips = kwargs.get('allowed_ips')

        self.interface = Interface()
        self.dev = IPRoute()

    def __repr__(self):
        return "\ndevice_id='%s', \nip='%s', \ndevice_pw='%s', \nuser_pw='%s', \nwgprvkey='%s', \nwgpubkey='%s'," \
               "\ndoa='%s', \ndod='%s', \nhw_model='%s', \nhw_version='%s', \nsw_version='%s', \nblocked='%s'," \
               "\ngateway='%s', \nlistenport='%s', \nendpoint='%s', \nallowed_ips='%s'" % (
            self.device_id, self.ip, self.device_pw, self.user_pw, self.wgprvkey, self.wgpubkey, self.doa, self.dod,
            self.hw_model, self.hw_version, self.sw_version, self.blocked, self.gateway, self.listenport,
            self.endpoint, self.allowed_ips)


class Gateway(Base):

    __tablename__ = 'gateway'

    id = Column(Integer, Sequence('gw_id_seq'), primary_key=True)
    name = Column('name', String(32), unique=True)
    os = Column('os', String(32), default=None)
    ip = Column('ip', String(32), unique=True)
    host = Column('host', String(32), default=None)
    domain = Column('domain', String(32), default=None)
    tld = Column('tld', String(32), default=None)
    active = Column('active', Boolean, default=False)
    counter = Column('counter', Integer, default=0)

    router = relationship("Router", back_populates='gateway')

    network_id = Column(Integer, ForeignKey('network.id'))
    network = relationship("Network", back_populates="gateway")

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.os = kwargs.get('os')
        self.ip = kwargs.get('ip')
        self.host = kwargs.get('host')
        self.domain = kwargs.get('domain')
        self.tld = kwargs.get('tld')
        self.active = kwargs.get('active')

    def __repr__(self):
        return "name='%s', os='%s', ip='%s', host='%s', domain='%s', tld='%s', router='%s'" % (
                                self.name, self.os, self.ip, self.host, self.domain, self.tld, self.router)


class Network(Base):

    __tablename__ = 'network'

    id = Column(Integer, Sequence('nw_id_seq'), primary_key=True)
    name = Column('name', String(32), unique=True)
    enabled = Column('enabled', Boolean, default=False)
    gateway = relationship("Gateway", back_populates='network')
    router = relationship("Router", back_populates='network')

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.enabled = kwargs.get('enabled')

    def __repr__(self):
        return "name='%s', enabled='%s'" % (self.name, self.enabled)

