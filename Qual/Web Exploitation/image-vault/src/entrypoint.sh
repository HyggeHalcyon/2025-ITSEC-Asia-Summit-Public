#!/bin/sh

# Secure entrypoint
chmod 600 /entrypoint.sh

function genPass() {
    echo -n $RANDOM | sha256sum | head -c 64
}

# Set environment variables
export ADMIN_PASSWORD=$(genPass)
export FLAG="ITSEC{ch41n1n9_th3_vuln_t0g3th3rr}"

# Launch supervisord
/usr/bin/supervisord -c /etc/supervisord.conf