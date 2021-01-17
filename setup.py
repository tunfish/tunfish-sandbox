# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = [
    'autobahn',
    'crossbar',
    'SQLAlchemy-Utils',
    'SQLAlchemy==1.3.22',
    'psycopg2-binary',
    'pyroute2',
    'msgpack==1.0.0',
    'pysodium',
    'python-iptables',
    'cryptography>=2.7',
    'six>=1.13.0',
]

extras = {
}

setup(name='tunfish',
      version='0.1.0',
      description='Convenient VPN infrastructure on top of secure WireGuard tunnels',
      long_description=README,
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Object Brokering",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
        ],
      author='The Tunfish Developers',
      author_email='hello@tunfish.org',
      url='https://github.com/tunfish/tunfish-system',
      keywords='',
      #package_dir={'': ''},
      #packages=find_packages(),
      include_package_data=True,
      package_data={
      },
      zip_safe=False,
      test_suite='tunfish.test',
      install_requires=requires,
      extras_require=extras,
      dependency_links=[
      ],
      entry_points={
          'console_scripts': [
              'tf-client           = tunfish.main:start_client',
              'tf-gateway          = tunfish.main:start_gateway',
              'tf-server           = tunfish.main:start_server',
              'tf-ctl              = tunfish.main:tf_control',
              'tf-web              = tunfish.main:tf_web',
          ],
      },
)
