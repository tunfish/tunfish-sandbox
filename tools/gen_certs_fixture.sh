# CA
echo "generate ca.key"
openssl genrsa -aes256 -out ca.key 4096
echo "generate ca.pem"
openssl req -new -x509 -nodes -key ca.key -out ca.pem -days 1000

# crossbar
echo "generate crossbar.key"
openssl genrsa -out crossbar.key 4096
echo "generate crossbar.csr"
openssl req -new -key crossbar.key -out crossbar.csr
echo "generate crossbar.pem"
openssl x509 -CA ca.pem -CAkey ca.key -CAcreateserial -req -in crossbar.csr -out crossbar.pem -days 365

# portier
echo "generate server.key"
openssl genrsa -out server.key 4096
echo "generate server.csr"
openssl req -new -key server.key -out server.csr
echo "generate server.pem"
openssl x509 -CA ca.pem -CAkey ca.key -CAcreateserial -req -in server.csr -out server.pem -days 365

# gateone
echo "generate gateone.key"
openssl genrsa -out gateone.key 4096
echo "generate gateone.csr"
openssl req -new -key gateone.key -out gateone.csr
echo "generate gateone.pem"
openssl x509 -CA ca.pem -CAkey ca.key -CAcreateserial -req -in gateone.csr -out gateone.pem -days 365

# tf-0815
echo "generate tf-0815.key"
openssl genrsa -out tf-0815.key 4096
echo "generate tf-0815.csr"
openssl req -new -key tf-0815.key -out tf-0815.csr
echo "generate tf-0815.pem"
openssl x509 -CA ca.pem -CAkey ca.key -CAcreateserial -req -in tf-0815.csr -out tf-0815.pem -days 365

# tf-ctl
echo "generate tf-ctl.key"
openssl genrsa -out tf-ctl.key 4096
echo "generate tf-ctl.csr"
openssl req -new -key tf-ctl.key -out tf-ctl.csr
echo "generate tf-ctl.pem"
openssl x509 -CA ca.pem -CAkey ca.key -CAcreateserial -req -in tf-ctl.csr -out tf-ctl.pem -days 365