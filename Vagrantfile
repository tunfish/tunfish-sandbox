ENV['VAGRANT_DEFAULT_PROVIDER'] = 'libvirt'

$script = <<-'SCRIPT'
echo "deb http://deb.debian.org/debian/ buster-backports main" > /etc/apt/sources.list.d/wireguard.list
#printf 'Package: *\nPin: release a=unstable\nPin-Priority: 90\n' > /etc/apt/preferences.d/limit-unstable
apt update
#sudo apt-get -yq install linux-headers-amd64
#sudo apt-get -yq --no-install-suggests --no-install-recommends --allow-unauthenticated install wireguard
sudo apt-get -yq --allow-unauthenticated install wireguard
# cd /vagrant/
# sudo python3 -E /vagrant/setup.py develop
SCRIPT



Vagrant.configure("2") do |config|

# debian 10 testing environment
  config.vm.define "tf-debian10" do |crossbar|
    crossbar.vm.box = "generic/debian10"
    crossbar.vm.hostname = 'tf-debian10'
    crossbar.vm.box_url = "generic/debian10"

    crossbar.vm.box_version = "3.0.8"

    # Crossbar is running on the public network.
    crossbar.vm.network :private_network, ip: "172.16.255.2", netmask: '255.255.0.0'

    crossbar.vm.synced_folder ".", "/vagrant"
    crossbar.vm.provider :libvirt do |v|
      v.memory="512"
      v.storage :file, :size => '4G'
    end

    ## For masterless, mount your salt file root ???
    crossbar.vm.synced_folder "./salt/roots/salt/", "/srv/salt/"
    crossbar.vm.synced_folder "./salt/roots/pillar/", "/srv/pillar/"



    config.vm.provision :salt do |salt|
      salt.masterless = true
      salt.run_highstate = true
      salt.verbose = true
      salt.python_version = "3"
      salt.bootstrap_script = "setup-salt.sh"
    end

    crossbar.vm.provision "shell", inline: $script
  end


  config.vm.define "tf-crossbar" do |crossbar|
    crossbar.vm.box = "generic/debian10"
    crossbar.vm.hostname = 'tf-crossbar'
    crossbar.vm.box_url = "generic/debian10"

    crossbar.vm.box_version = "3.0.30"

    # Crossbar is running on the public network.
    crossbar.vm.network :private_network, ip: "172.16.42.2", netmask: '255.255.0.0'

    crossbar.vm.synced_folder ".", "/vagrant"

    # salt bootstrap
    crossbar.vm.provision "shell", inline: "sh /vagrant/setup-salt.sh"

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

    crossbar.vm.provision "shell", inline: $script

  end

  config.vm.define "tf-portier" do |portier|
    portier.vm.box = "generic/debian10"
    portier.vm.hostname = 'tf-portier'
    portier.vm.box_url = "generic/debian10"

    portier.vm.box_version = "3.0.30"

    portier.vm.synced_folder ".", "/vagrant"

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

    portier.vm.provision "shell", inline: $script

  end

  config.vm.define "tf-gateway-1" do |gateone|
    gateone.vm.box = "generic/debian10"
    gateone.vm.hostname = 'tf-gateway-1'
    gateone.vm.box_url = "generic/debian10"

    gateone.vm.box_version = "3.0.30"

    gateone.vm.synced_folder ".", "/vagrant"

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

    gateone.vm.provision "shell", inline: $script

  end


  config.vm.define "tf-client-1" do |client|
    client.vm.box = "generic/debian10"
    client.vm.hostname = 'tf-client-1'
    client.vm.box_url = "generic/debian10"

    client.vm.box_version = "3.0.30"

    client.vm.synced_folder ".", "/vagrant"

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

    client.vm.provision "shell", inline: $script

  end

end
