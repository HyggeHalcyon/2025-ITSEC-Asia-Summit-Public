docker build -t shanghai .
# change the host port as you like
# also, consider updating HTTP_PORT if the public port is different from 8545
docker run -p 31337:31337 -p 8545:8545 shanghai
