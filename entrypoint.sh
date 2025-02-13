#!/bin/sh

# Loop through all *.conf.template files in the /etc directory (or any other relevant directory)
for template in /etc/wireguard/*.conf.template; do
  # For each template, use envsubst to create a *.conf file
  envsubst < "$template" > "${template%.template}"
done

# Now run the main services
tinyproxy &
/venv/bin/python3 /api.py