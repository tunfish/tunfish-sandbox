Vagrant.configure("2") do |config|

  config.vm.define "tf-crossbar" do |crossbar|
    crossbar.vm.box = "generic/debian9"
    crossbar.vm.hostname = 'tf-crossbar'
    crossbar.vm.box_url = "generic/debian9"

    # Crossbar is running on the public network.
    crossbar.vm.network :private_network, ip: "192.168.42.1"

    config.vm.synced_folder ".", "/vagrant"

    crossbar.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--name", "tf-crossbar"]
    end

    ## For masterless, mount your salt file root ???
    config.vm.synced_folder "./salt/roots/salt/", "/srv/salt/"
    config.vm.synced_folder "./salt/roots/pillar/", "/srv/pillar/"

    config.vm.provision :salt do |salt|
      salt.masterless = true
      salt.run_highstate = true
      salt.verbose = true
    end

  end

  config.vm.define "tf-portier" do |portier|
    portier.vm.box = "generic/debian9"
    portier.vm.hostname = 'tf-portier'
    portier.vm.box_url = "generic/debian9"

    config.vm.box_version = "2.0.0"

    config.vm.synced_folder ".", "/vagrant"

    # Portier is running in DMZ.
    portier.vm.network :private_network, ip: "192.168.23.1"

    portier.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--name", "tf-portier"]
    end

    ## For masterless, mount your salt file root ???
    config.vm.synced_folder "./salt/roots/salt/", "/srv/salt/"
    config.vm.synced_folder "./salt/roots/pillar/", "/srv/pillar/"

    config.vm.provision :salt do |salt|
      salt.masterless = true
      salt.run_highstate = true
      salt.verbose = true
    end

  end

  config.vm.define "tf-gateway-1" do |gateone|
    gateone.vm.box = "generic/debian9"
    gateone.vm.hostname = 'tf-gateway-1'
    gateone.vm.box_url = "generic/debian9"

    config.vm.box_version = "2.0.0"

    config.vm.synced_folder ".", "/vagrant"

    # Wireguard gateways are also on the public network.
    gateone.vm.network :private_network, ip: "192.168.42.50"

    gateone.vm.provider :virtualbox do |v|
      #v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      #v.customize ["modifyvm", :id, "--memory", 512]
      #v.customize ["modifyvm", :id, "--name", "tf-gateway-1"]
    end

    ## For masterless, mount your salt file root ???
    config.vm.synced_folder "./salt/roots/salt/", "/srv/salt/"
    config.vm.synced_folder "./salt/roots/pillar/", "/srv/pillar/"

    config.vm.provision :salt do |salt|
      salt.masterless = true
      salt.run_highstate = true
      salt.verbose = true
    end

  end


  config.vm.define "tf-client-1" do |srv|
    srv.vm.box = "generic/debian9"
    srv.vm.hostname = 'tf-client-1'
    srv.vm.box_url = "generic/debian9"

    config.vm.box_version = "2.0.0"

    config.vm.synced_folder ".", "/vagrant"

    # This is the roadwarrior client.
    srv.vm.network :private_network, ip: "192.168.100.10"

    srv.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--name", "tf-client-1"]
    end

    ## For masterless, mount your salt file root ???
    config.vm.synced_folder "./salt/roots/salt/", "/srv/salt/"
    config.vm.synced_folder "./salt/roots/pillar/", "/srv/pillar/"

    config.vm.provision :salt do |salt|
      salt.masterless = true
      salt.run_highstate = true
      salt.verbose = true
    end

  end

end
