ENV['VAGRANT_DEFAULT_PROVIDER'] = 'libvirt'

$install_wireguard = <<-'SCRIPT'
    # install wireguard
    echo "deb http://deb.debian.org/debian/ buster-backports main" > /etc/apt/sources.list.d/wireguard.list
    sudo apt update
    sudo apt-get -yq --allow-unauthenticated install wireguard
SCRIPT

#$script_node = <<-'SCRIPT'
#    source /home/vagrant/.venv/bin/activate
#    pip install -e /vagrant/node
#SCRIPT

$portier_database = <<-'SCRIPT'
    # create database
    sh /vagrant/sandbox/tools/create_db_user.sh
SCRIPT

$install_dependencies = <<-'SCRIPT'
    # python3 -m venv /home/vagrant/.venv
    # chown -R vagrant:vagrant /home/vagrant/.venv
    # source /home/vagrant/.venv/bin/activate
    cd /vagrant/sandbox/
    python3 setup.py develop
SCRIPT

Vagrant.configure("2") do |config|

  config.vm.define "tf-crossbar" do |crossbar|
    #crossbar.vm.box = "debian/testing64"
    crossbar.vm.box = "generic/debian10"
    crossbar.vm.hostname = "tf-crossbar"
    #crossbar.vm.box_url = "debian/testing64"
    crossbar.vm.box_url = "generic/debian10"

    #crossbar.vm.box_version = "20210124.1"
    #crossbar.vm.box_version = "20200607.1"
    crossbar.vm.box_version = "3.2.2"

    # Crossbar is running on the public network.
    crossbar.vm.network :private_network, ip: "172.16.42.2", netmask: '255.255.0.0'

    crossbar.vm.synced_folder "../", "/vagrant", type: "nfs", nfs_version: 4, nfs_udp: false, mount_options: ["rw", "vers=4", "tcp", "nolock"]

    # salt bootstrap
    crossbar.vm.provision "shell", inline: "sh /vagrant/sandbox/tools/setup-salt.sh"

    # setup.py
    # crossbar.vm.provision "shell", inline: "python3 /vagrant/setup.py develop"

    crossbar.vm.provider :libvirt do |v|
      #v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      #v.customize ["modifyvm", :id, "--memory", 512]
      #v.customize ["modifyvm", :id, "--name", "tf-crossbar"]
      v.memory="512"
      v.storage :file, :size => '8G'
    end

    ## For masterless, mount your salt file root ???
    config.vm.synced_folder "./salt/roots/salt/", "/srv/salt/"
    config.vm.synced_folder "./salt/roots/pillar/", "/srv/pillar/"

    config.vm.provision :salt do |salt|
      salt.masterless = true
      salt.run_highstate = true
      salt.verbose = true
      salt.python_version = "3"
      #salt.bootstrap_script = "setup-salt.sh"
    end

    crossbar.vm.provision "shell", inline: $install_dependencies

  end

  config.vm.define "tf-portier" do |portier|
    portier.vm.box = "generic/debian10"
    portier.vm.hostname = 'tf-portier'
    portier.vm.box_url = "generic/debian10"

    portier.vm.box_version = "3.1.18"

    portier.vm.synced_folder "../", "/vagrant"

    # salt bootstrap
    portier.vm.provision "shell", inline: "sh /vagrant/sandbox/tools/setup-salt.sh"

    # Portier is running in DMZ.
    portier.vm.network :private_network, ip: "172.16.23.2", netmask: "255.255.0.0"

    portier.vm.provider :libvirt do |v|
      #v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      #v.customize ["modifyvm", :id, "--memory", 512]
      #v.customize ["modifyvm", :id, "--name", "tf-portier"]
      v.memory="512"
      v.storage :file, :size => '8G'
      #v.name="tf-portier"
      #v.natdnshostresolver1="on"

    end

    ## For masterless, mount your salt file root ???
    config.vm.synced_folder "./salt/roots/salt/", "/srv/salt/"
    config.vm.synced_folder "./salt/roots/pillar/", "/srv/pillar/"

    config.vm.provision :salt do |salt|
      salt.masterless = true
      salt.run_highstate = true
      salt.verbose = true
      salt.python_version = "3"
      #salt.bootstrap_script = "setup-salt.sh"
    end

    portier.vm.provision "shell", inline: $install_dependencies
    portier.vm.provision "shell", inline: $portier_database

  end

  config.vm.define "tf-gateway-1" do |gateone|
    gateone.vm.box = "generic/debian10"
    gateone.vm.hostname = 'tf-gateway-1'
    gateone.vm.box_url = "generic/debian10"

    gateone.vm.box_version = "3.1.18"

    gateone.vm.synced_folder "../", "/vagrant"

    # salt bootstrap
    gateone.vm.provision "shell", inline: "sh /vagrant/sandbox/tools/setup-salt.sh"

    # Wireguard gateways are also on the public network.
    gateone.vm.network :private_network, ip: "172.16.42.50", netmask: "255.255.0.0"

    gateone.vm.provider :libvirt do |v|
      #v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      #v.customize ["modifyvm", :id, "--memory", 512]
      #v.customize ["modifyvm", :id, "--name", "tf-gateway-1"]
      v.memory="512"
      v.storage :file, :size => '8G'
    end

    ## For masterless, mount your salt file root ???
    config.vm.synced_folder "./salt/roots/salt/", "/srv/salt/"
    config.vm.synced_folder "./salt/roots/pillar/", "/srv/pillar/"

    config.vm.provision :salt do |salt|
      salt.masterless = true
      salt.run_highstate = true
      salt.verbose = true
      salt.python_version = "3"
    ##  salt.bootstrap_script = "setup-salt.sh"
    end

    gateone.vm.provision "shell", inline: $install_wireguard
    gateone.vm.provision "shell", inline: $install_dependencies

  end


  config.vm.define "tf-client-1" do |client|
    client.vm.box = "generic/debian10"
    client.vm.hostname = 'tf-client-1'
    client.vm.box_url = "generic/debian10"

    client.vm.box_version = "3.1.18"

    client.vm.synced_folder "../", "/vagrant"

    # salt bootstrap
    client.vm.provision "shell", inline: "sh /vagrant/sandbox/tools/setup-salt.sh"

    # This is the roadwarrior client.
    client.vm.network :private_network, ip: "172.16.100.10", netmask: "255.255.0.0"

    client.vm.provider :libvirt do |v|
      # v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      # v.customize ["modifyvm", :id, "--memory", 512]
      # v.customize ["modifyvm", :id, "--name", "tf-client-1"]
      v.memory="512"
      v.storage :file, :size => '8G'
    end

    ## For masterless, mount your salt file root ???
    config.vm.synced_folder "./salt/roots/salt/", "/srv/salt/"
    config.vm.synced_folder "./salt/roots/pillar/", "/srv/pillar/"

    config.vm.provision :salt do |salt|
      salt.masterless = true
      salt.run_highstate = true
      salt.verbose = true
      salt.python_version = "3"
      #salt.bootstrap_script = "setup-salt.sh"
    end

    client.vm.provision "shell", inline: $install_wireguard
    client.vm.provision "shell", inline: $install_dependencies
  end

end
