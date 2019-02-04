.. image:: https://img.shields.io/github/tag/tunfish/tunfish-system.svg
    :target: https://github.com/tunfish/tunfish-system
.. image:: https://img.shields.io/badge/platform-Linux%20%7C%20OpenWRT%20%7C%20LEDE-blue.svg
    :target: #
.. image:: https://img.shields.io/badge/technologies-WireGuard%20%7C%20Netlink%20%7C%20WAMP%20%7C%20Websocket-blue.svg
    :target: #

|

.. image:: https://ptrace.tunfish.org/thunfisch-160.jpg
    :target: #


##################
The Tunfish System
##################

*****
About
*****
Create a convenient VPN infrastructure
on top of secure WireGuard_ tunnels.


*****
Howto
*****
This runbook will guide you through the process of setting
up an appropriate testbed environment. It will provision
a number of Vagrant machines and configure them to talk
to each other in order.

After that, you will easily be able to conduct connectivity
tests and continue with further experiments.


*****
Setup
*****
This section will guide you through setting up
a development/testing sandbox on your machine.

Acquire source repository::

    git clone https://github.com/tunfish/tunfish-system

Make Vagrant provision and spin up all machines configured in this environment::

    vagrant up


**************
Network layout
**************
There are three machines ``"tf-crossbar"``, ``"tf-portier"``, ``"tf-gateway-1"`` and
``"tf-client-1"``, completely provisioned by Vagrant.

Here is a short overview as an introduction.
Please read this section carefully.


Machines
========
Public facing hosts::

    192.168.42.1        WAMP broker
    192.168.42.50       Gateway server 1

DMZ hosts::

    192.168.23.1        Portier server

VPN clients::

    192.168.100.10      Client 1


*****
Usage
*****

Login to each virtual machine::

    vagrant ssh tf-crossbar
    vagrant ssh tf-portier
    vagrant ssh tf-gateway-1
    vagrant ssh tf-client-1


***********
Development
***********
To repeat the virtual machine provisioning, run::

    vagrant up --provision

To reprovision just a single host, use::

    vagrant up --provision tf-portier

The repository root will be mounted into each virtual machine at
``/opt/tunfish-system`` for convenient live editing.

Please be ware to invoke ``vagrant reload`` when making changes
within the ``./salt`` directory, if something is fishy.


*******************
Project information
*******************

About
=====
The "Tunfish sandbox" spike is released under the GNU AGPL license.
Its source code lives on `GitHub <https://github.com/tunfish/tunfish-system>`_.

If you'd like to contribute you're most welcome!
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue.

Thanks in advance for your efforts, we really appreciate any help or feedback.

License
=======
Licensed under the GNU AGPL license. See LICENSE_ file for details.

.. _LICENSE: https://github.com/tunfish/tunfish-system/blob/master/LICENSE



****************
Acknowledgements
****************

Tunfish would not have been possible without these awesome people:

- Jason Donenfeld for conceiving and building WireGuard_. After reading
  the introduction `[RFC] WireGuard: next generation secure network tunnel`_
  in late 2016 and quickly scanning his `paper about WireGuard`_, nobody
  wondered that WireGuard rapidly gained attraction.

- `Tobias Oberstein`_ for conceiving the `Web Application Messaging Protocol`_ (WAMP)
  and its implementation through `Crossbar.io`_ and Autobahn_, along with all
  other contributors to it.

- `Mike Bayer`_ for conceiving the excellent Python SQL Toolkit and
  Object Relational Mapper SQLAlchemy_.

- `Peter V. Saveliev`_ for creating the `pyroute2 netlink framework`_ and
  @ldx for `python-iptables`_.

- Mitchell Hashimoto, Chris Roberts and the countless other `contributors to Vagrant`_
  for conceiving and maintaining Vagrant_.

- Thomas Hatch, Pedro Algarvio, Erik Johnson, Nicole Thomas and all the
  other `contributors to Salt`_ for conceiving and maintaining Salt_.

- Countless other authors of packages from the Python
  ecosystem and beyond for gluing everything together.

Thank you so much for providing such great infrastructure
components and resources to the community! You know who you are.


***************
Troubleshooting
***************
If you encounter any problems during setup, we may humbly
refer you to the `<doc/troubleshooting.rst>`_ documentation.


----

Have fun!


.. _WireGuard: https://www.wireguard.com/

.. _[RFC] WireGuard\: next generation secure network tunnel: https://lkml.org/lkml/2016/6/28/629
.. _paper about WireGuard: https://www.wireguard.com/papers/wireguard.pdf

.. _Web Application Messaging Protocol: https://wamp-proto.org/
.. _Crossbar.io: https://crossbar.io/
.. _Autobahn: https://crossbar.io/autobahn/

.. _Mike Bayer: https://github.com/zzzeek
.. _SQLAlchemy: https://www.sqlalchemy.org/

.. _Peter V. Saveliev: https://github.com/svinota
.. _pyroute2 netlink framework: https://pyroute2.org/
.. _python-iptables: https://github.com/ldx/python-iptables

.. _Vagrant: https://www.vagrantup.com/
.. _Salt: https://en.wikipedia.org/wiki/Salt_(software)
.. _contributors to Vagrant: https://github.com/hashicorp/vagrant/graphs/contributors
.. _contributors to Salt: https://github.com/saltstack/salt/graphs/contributors
