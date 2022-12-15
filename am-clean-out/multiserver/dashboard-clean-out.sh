#!/usr/bin/env bash

set -a

if grep Ubuntu /etc/os-release >/dev/null; then
  DASHBOARD_CONFIG_FILE=/etc/default/archivematica-dashboard
else
  DASHBOARD_CONFIG_FILE=/etc/sysconfig/archivematica-dashboard
fi

# Import environment variables from config file
source ${DASHBOARD_CONFIG_FILE}

# Stop AM services
echo -e "Stopping AM services\n"
sudo service archivematica-mcp-server stop
sudo service archivematica-mcp-client stop
sudo service archivematica-dashboard stop

if grep Ubuntu /etc/os-release >/dev/null; then
  DASHBOARD_CONFIG_FILE=/etc/default/archivematica-dashboard
else
  DASHBOARD_CONFIG_FILE=/etc/sysconfig/archivematica-dashboard
fi

# Run purge_transient_processing_data on pipeline

sudo -u archivematica bash -c " \
    set -a
    source /etc/default/archivematica-dashboard > /dev/null 2>&1 || \
        source /etc/sysconfig/archivematica-dashboard > /dev/null 2>&1 \
            || (echo 'Environment file not found'; exit 1)
    cd /usr/share/archivematica/dashboard
    /usr/share/archivematica/virtualenvs/archivematica/bin/python \
        manage.py purge_transient_processing_data --purge-unknown --age '0 00:00:00'
";

# Delete all Elasticsearch indices
curl -XDELETE "${ARCHIVEMATICA_DASHBOARD_DASHBOARD_ELASTICSEARCH_SERVER}/aips" > /dev/null 2> /dev/null
curl -XDELETE "${ARCHIVEMATICA_DASHBOARD_DASHBOARD_ELASTICSEARCH_SERVER}/aipfiles" > /dev/null 2> /dev/null
curl -XDELETE "${ARCHIVEMATICA_DASHBOARD_DASHBOARD_ELASTICSEARCH_SERVER}/transfers" > /dev/null 2> /dev/null
curl -XDELETE "${ARCHIVEMATICA_DASHBOARD_DASHBOARD_ELASTICSEARCH_SERVER}/transferfiles" > /dev/null 2> /dev/null

# Start AM services
echo -e "\nStarting AM services\n"
sudo service archivematica-mcp-server start
sudo service archivematica-mcp-client start
sudo service archivematica-dashboard start

