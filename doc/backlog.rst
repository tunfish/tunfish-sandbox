Sandbox
=======
- Make sandboxing actually work by resolving Debian9/10 vs. Python3.5/3.7 vs. Salt stuff.
- Make Vagrant sandboxing unisex re. VirtualBox vs. libvirt

Code
====
- Add key provisioner script
    - crossbar.key
    - portier.key

- Improve asset loading (certs, keys, config)
- Add better command line parser
- Add logging
- Add ``setup.py`` with script entrypoints
- Nail current Python dependencies
- Add fixtures to gendb.py, also for Gateway

Code refactoring
================
- Refactor sasu tools
- ``tunfish.network.wireguard``: Adapt key-format re. wg_genkey vs. b64encode and use vanilla version
	- https://gist.github.com/artizirk/3a8efeee33fce34baf6047aed7205a2e
	- https://github.com/svinota/pyroute2/blob/master/pyroute2/netlink/generic/wireguard.py
