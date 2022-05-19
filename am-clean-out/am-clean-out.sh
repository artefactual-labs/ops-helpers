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
sudo service archivematica-storage-service stop
sudo service archivematica-mcp-server stop
sudo service archivematica-mcp-client stop
sudo service archivematica-dashboard stop

if grep Ubuntu /etc/os-release >/dev/null; then
  SS_CONFIG_FILE=/etc/default/archivematica-storage-service
  DASHBOARD_CONFIG_FILE=/etc/default/archivematica-dashboard
else
  SS_CONFIG_FILE=/etc/sysconfig/archivematica-storage-service
  DASHBOARD_CONFIG_FILE=/etc/sysconfig/archivematica-dashboard
fi

if grep SS_DB_URL=mysql ${SS_CONFIG_FILE}>/dev/null; then
  # MySQL SS database
  SS_DATABASE_NAME=$(grep -oP '^SS_DB_URL.*\/\K\w+$' ${SS_CONFIG_FILE})
  SQL_COMMAND="mysql ${SS_DATABASE_NAME} --batch -s -N -e"
else
  # SQLite3 SS database
  echo ".mode tabs" > /tmp/sqlite3rc
  SS_DB_NAME=$(grep -oP '^SS_DB_NAME\s*=\K[^;]*' ${SS_CONFIG_FILE})
  SQL_COMMAND="sqlite3 ${SS_DB_NAME} -init /tmp/sqlite3rc"
fi

# Take SS and MySQL backups
if grep SS_DB_URL=mysql ${SS_CONFIG_FILE}>/dev/null; then
  echo -e "Taking MySQL backups\n"
  mysqldump SS > /tmp/SS.sql
  mysqldump MCP > /tmp/MCP.sql
else
  echo -e "Taking MySQL and sqlite3 backups\n"
  mysqldump MCP > /tmp/MCP.sql
  cp ${SS_DB_NAME} /tmp/$(basename ${SS_DB_NAME})
fi

# Get spaces
while IFS=$'\t' read uuid path;do

  # Get space's locations
  while IFS=$'\t' read relative_path ;do
     echo -e "Deleting the location: ${path%/}/${relative_path%/}/*\n"
     rm -rf ${path%/}/${relative_path%/}/* > /dev/null 2>&1

  done < <(${SQL_COMMAND} "select relative_path from locations_location where ( purpose='DS' or purpose='AS' or purpose='BL' or purpose='AR' or purpose='RP' or purpose='SS') and space_id=\"${uuid}\"")

done  < <(${SQL_COMMAND} "select uuid,path from locations_space where access_protocol='FS'")

# Truncate SS tables

if grep SS_DB_URL=mysql ${SS_CONFIG_FILE}>/dev/null; then
  # MySQL SS database
  echo -e "Truncating SS tables (MySQL)\n"
  ${SQL_COMMAND} "SET FOREIGN_KEY_CHECKS=0;\
	  truncate table locations_event; \
          truncate table locations_file; \
          truncate table locations_fixitylog; \
          truncate table locations_package; \
          truncate table locations_package_related_packages; \
          SET FOREIGN_KEY_CHECKS=1;"
else
  # SQLite3 SS database
  echo -e "Truncating SS tables (sqlite3)\n"
  ${SQL_COMMAND} "PRAGMA foreign_keys = OFF;\
	  truncate table locations_event; \
          truncate table locations_file; \
          truncate table locations_fixitylog; \
          truncate table locations_package; \
          truncate table locations_package_related_packages; \
	  PRAGMA foreign_keys = ON;"
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
sudo service archivematica-storage-service start
sudo service archivematica-mcp-server start
sudo service archivematica-mcp-client start
sudo service archivematica-dashboard start

