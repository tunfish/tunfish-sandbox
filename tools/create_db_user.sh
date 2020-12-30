sudo -u postgres psql -c "CREATE DATABASE tunfishdb"
sudo -u postgres psql -c "CREATE USER tfuser WITH ENCRYPTED PASSWORD 'dbpw'"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE tunfishdb TO tfuser"
