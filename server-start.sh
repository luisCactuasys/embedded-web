#!/bin/bash

# Initialize PWM0 before server start
# Make sure the other script is executable (chmod +x setup_environment.sh)
echo "Running pwminit.sh..."
$PWD/pwminit.sh

# Start the Lighttpd server
echo "Starting Lighttpd server..."
sudo lighttpd -D -f server-test.conf

