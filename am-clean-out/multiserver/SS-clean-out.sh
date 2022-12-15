#!/usr/bin/env bash

set -a

# Stop AM services
echo -e "Stopping SS service\n"
sudo service archivematica-storage-service stop

if grep Ubuntu /etc/os-release >/dev/null; then
  SS_CONFIG_FILE=/etc/default/archivematica-storage-service
else
  SS_CONFIG_FILE=/etc/sysconfig/archivematica-storage-service
fi

if grep SS_DB_URL=mysql ${SS_CONFIG_FILE}>/dev/null; then
  # MySQL SS database
  # See regexp here: https://gist.github.com/knadh/5be315f877530eab3c8fc1fd2708d191
  SS_DATABASE_NAME=$(grep -oP '^SS_DB_URL.*\/\K\w+$' ${SS_CONFIG_FILE})
  SS_DATABASE_HOST=$(grep -oP "^SS_DB_URL.*://.*@\K(.+?):" ${SS_CONFIG_FILE} | cut -d: -f1)
  SS_DATABASE_PORT=$(grep -oP "^SS_DB_URL.*://.*@.*:\K(\d+)/" ${SS_CONFIG_FILE} | cut -d/ -f1)
  SS_DATABASE_USER=$(grep -oP "^SS_DB_URL.*://\K(.+?):" ${SS_CONFIG_FILE} | cut -d: -f1)
  SS_DATABASE_PASSWORD=$(grep -oP "^SS_DB_URL.*://.*:\K(.+?)@" ${SS_CONFIG_FILE} | cut -d@ -f1)
  SQL_OPTIONS="--user=${SS_DATABASE_USER} --password=${SS_DATABASE_PASSWORD} --host=${SS_DATABASE_HOST} --port=${SS_DATABASE_PORT}"
  SQL_COMMAND="mysql ${SQL_OPTIONS} ${SS_DATABASE_NAME} --batch -s -N -e"

else
  # SQLite3 SS database
  echo ".mode tabs" > /tmp/sqlite3rc
  SS_DB_NAME=$(grep -oP '^SS_DB_NAME\s*=\K[^;]*' ${SS_CONFIG_FILE})
  SQL_COMMAND="sqlite3 ${SS_DB_NAME} -init /tmp/sqlite3rc"
fi

# Take SS and MySQL backups
if grep SS_DB_URL=mysql ${SS_CONFIG_FILE}>/dev/null; then
  echo -e "Taking MySQL backups\n"
  mysqldump ${SQL_OPTIONS} --password='${SS_DATABASE_PASSWORD}' --no-tablespaces ${SS_DATABASE_NAME} > /tmp/SS.sql
else
  echo -e "Taking sqlite3 backups\n"
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

# Reset the 'used' counter when purpose is different than TS (Trasnfer Source)
${SQL_COMMAND} "update locations_location set used = 0 where purpose != 'TS'"

# Start SS service
echo -e "\nStarting SS service\n"
sudo service archivematica-storage-service start

