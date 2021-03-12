#uptodate:
#  pkg.uptodate:
#    - refresh: False
#    - dist_upgrade: False

required_packages:
  pkg.installed:
    - names:
      - python3
      - postgresql-11
      - postgresql-server-dev-11
      - libsnappy-dev
      #- nginx

python-pip:
  pkg.installed:
    - pkgs:
      - python-pip
      - python3-pip

#virtualenv:
#  pip.installed:
#    - name: virtualenv
#    - bin_env: '/usr/bin/pip3'
#    - require:
#      - pkg: python-pip

#tf-env:
#  virtualenv.managed:
#    - name: /home/vagrant/venv
#    - cwd: /home/vagrant/venv/bin
#    - system_site_packages: True

#python_requirements:
#  pip.installed:
#    - requirements: salt://pythonrequirements/files/requirements.txt
#    - bin_env: /home/vagrant/venv/
#    - pip_bin: /home/vagrant/venv/bin/pip3
#  {% set pythonrequirements=[] %}
#  {% for r in pillar["requirements"]["python"] %}
#  {% do pythonrequirements.append(r) %}
#  {% endfor %}
#python_requirements:
#  pip.installed:
#    - pkgs:
#        {%- for r in pillar["requirements"]["python"] %}
#        - {{r}}
#        {%- endfor %}
#    - bin_env: /home/vagrant/venv/
#    - pip_bin: /home/vagrant/venv/bin/pip3
