#!/bin/bash

#Requirements
# Run this script as an user with sudo provileges
# Create the file list: 
# a) When all AIPs are in the same dir: ls -1a $AIP_DIR 
# b) When every AIP is located on a differenrt directory (AM storage): find | grep 7z | sed 's/^\.\///g' > ../aip_files_list.txt

PIPELINE_UUID=1cd89413-e9ad-4838-966b-eb904468e450
AIP_STORE_LOCATION_UUID=dd042c75-95b8-46c5-a84c-d69d0b92f346
AIPS_FILES_LIST=aip_files_list.txt
AIP_DIR=/mnt/sto_processing/transfer/migration/aipstore
AIP_STORE_PATH=/mnt/sto_AIP_DIP/aipstore
AM_CONFIG_DIR=/etc/default # Use /etc/sysconfig on CentOS

AIP_TMP_DIR=/mnt/sto_processing/aip-import-tmp

ORANGE='\033[0;33m'
BLUE='\033[0;34m'
NOCOLOR='\033[0m'

while IFS= read -r aip_7z_file <&3;do
        #Import AIP
	echo -e "\n${BLUE}Importing AIP file: ${AIP_DIR}/${aip_7z_file}${NOCOLOR} - `date`"
	sudo chown archivematica:archivematica ${AIP_DIR}/${aip_7z_file}

	sudo -u archivematica bash -c " \
		set -a -e
		source ${AM_CONFIG_DIR}/archivematica-storage-service
		cd /usr/lib/archivematica/storage-service
		/usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/python manage.py \
		import_aip --decompress-source --compression-algorithm '7z with bzip' --force --pipeline \
		${PIPELINE_UUID} --aip-storage-location ${AIP_STORE_LOCATION_UUID} --tmp-dir ${AIP_TMP_DIR} \
		${AIP_DIR}/'${aip_7z_file}'
        ";
	#Abort when import_aip fails
	if [ $? -ne 0 ];then
                echo "Error when importing ${aip_7z_file} file: Aborting! - `date`"
		exit 1
        fi
        #Get AIP UUID from filename
	aip_uuid=$(echo ${aip_7z_file} | grep -Po '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
	#Abort when grep doesn't match an UUID
	if [ $? -ne 0 ];then
                echo "Error getting UUID from ${aip_7z_file} filename: Aborting! - `date`"
                exit 1
        fi
	#Index AIP with rebuild_elasticsearch_aip_index_from_files
	echo -e "\n${BLUE}Indexing from AIP file uuid: ${aip_uuid} ${NOCOLOR}- `date`"
	sudo -u archivematica bash -c " \
	    set -a -e
	    source ${AM_CONFIG_DIR}/archivematica-dashboard
	    cd /usr/share/archivematica/dashboard
	    /usr/share/archivematica/virtualenvs/archivematica/bin/python \
	        manage.py rebuild_elasticsearch_aip_index_from_files \
	            ${AIP_STORE_PATH} --delete --uuid=${aip_uuid}
	";
	#Abort when rebuild_elasticsearch_aip_index_from_files fails
	if [ $? -ne 0 ];then
                echo "Error when reindexing ${aip_7z_file} file: Aborting! - `date`"
                exit 1
        fi
done 3< $AIPS_FILES_LIST

