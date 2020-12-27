# channge salt repo
sudo sed -i s/apt/py3/g /etc/apt/sources.list.d/saltstack.list
# add key
wget -qO - https://repo.saltstack.com/py3/debian/10/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
# update repos
sudo apt update
# get salt-bootstrap
wget https://raw.githubusercontent.com/saltstack/salt-bootstrap/stable/bootstrap-salt.sh
# run salt-bootstrap
sudo sh bootstrap-salt.sh -x python3