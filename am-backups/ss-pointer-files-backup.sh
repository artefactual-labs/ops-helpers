#!/bin/bash
BACKUP_ROOT="/srv/ss-pf-backups"
BACKUP_TIME=`date +%Y%m%d-%H%M%S`
BACKUP_PATH="$BACKUP_ROOT/$BACKUP_TIME"
echo "Creating backups in $BACKUP_PATH ..."
mkdir -p $BACKUP_PATH

# this assumes the pointer files are stored in the default location
# (/var/archivematica/storage_service) (change the following variable if required)
SS_PF_LOCATION="/var/archivematica/storage_service"

find $SS_PF_LOCATION -type f -name "pointer.*.xml" -printf %P\\0 | tar -rvf $BACKUP_PATH/pointer_files.tar --directory $SS_PF_LOCATION -T -
