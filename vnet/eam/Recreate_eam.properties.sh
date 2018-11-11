#!/usr/bin/env bash

###
### Temporary script for TSE use only - delete after use - not maintained by VMware Inc. !!! ###
### See iKB #2148582
### Version 0.1709.1400
###

set -e

: ${EAMPROP:="/etc/vmware-eam/eam.properties"}

# Check file size
[ $(stat -c %s "${EAMPROP}") -ne 0 ] && read -p"WARNING: ${EAMPROP} is not empty! Press Ctrl-C now if you are not sure you want to continue!"
HOSTID="$(</etc/vmware/install-defaults/sca.hostid)"
[ -z "${HOSTID}" ] && echo "ERROR: Unable to get SCA HostID!" >&2 && exit 1
NOW="$(date +%Y%m%d-%H%M%S)"
FQDN_DEFAULT="$(hostname -f)"

read -p"Enter vCenter FQDN or IP address or press Enter to accept auto-detected value [${FQDN_DEFAULT}]: " FQDN
: ${FQDN:="${FQDN_DEFAULT}"}

cp -v "${EAMPROP}" "${EAMPROP}.backup-${NOW}"
cat >"${EAMPROP}" <<EOF
##############################################################################
# Copyright 2013-2014 VMware, Inc.  All rights reserved. VMware Confidential #
##############################################################################
# NOTE: This file was recreated on ${NOW} during SR session
vc.proxy.host=localhost
vc.proxy.port=80
# Hostname or IP of the EAM server
# Fill only if EAM is not running on the same host as VC
eam.host=
# EAM service port used to configure the HTTP connector of the application server.
eam.int.http.port=15005
# Port and scheme configuration which is used by the ESX 6.x hosts to reach EAM Vib
# file server.
eam.ext.port=443
eam.ext.scheme=https
# Port and scheme configuration which is used by the ESX 5.x hosts to reach EAM Vib
# file server.
eam.ext.port.deprecated=80
eam.ext.scheme.deprecated=http
eam.support_linked_clone=true
eam.clear_db_on_startup=false
eam.debug_ref_count=false
eam.recent_event_size=20
# Enable/disable VUM integration
vum.integration=true
# Value is specified in minutes (set to 24h = 1440m)
eam.scan_for_unknown_agent_vms=1440
# The timeout to wait for hostd to restart on a host (set to 5m=300s)
eam.hostd_restart_timeout=300
# The following entries will be added verbatim to the advanced options
# of hosts on which EAM is enabled. All are optional.
Net.DVFilterBindIpAddress=169.254.0.1
Net.TrafficFilterIpAddress=
#The IP for the VSWIF NIC on the dvFilter switch (for ESX classic).
Net.DVFilterVswifIpAddress=169.254.0.2
# Resource bundle configuration
eam.resourcebundle.filename=eam-resourcebundle.jar
# VLSI embedded tcServer configuration
#
tcserver.tmp.dir=/var/tmp/vmware/eam/tomcat
eam.web.root=/usr/lib/vmware-eam/web
# EAM SSL configuration
#
eam.keystore.type=VKS
eam.key.alias=vpxd-extension
eam.keystore.storename=vpxd-extension
# CM configuration
#
cm.url=http://localhost:18090/cm/sdk/?hostid=${HOSTID}
cm.wait.attempts=360
cm.wait.intervalSeconds=5
# SSO configuration
#
sso.wait.attempts=360
sso.wait.intervalSeconds=5
# VC SSL configuration
#
vc.truststore.type=VKS
vc.truststore.storename=TRUSTED_ROOTS
vc.tunnelSdkUri.template=https://##{VC_HOST_NAME}##:8089/sdk/vimService
vc.tunnelSdkUri=https://${FQDN}:8089/sdk/vimService
drs.demandCapacityRatio=100
EOF
