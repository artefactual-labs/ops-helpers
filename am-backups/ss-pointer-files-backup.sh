#!/bin/bash
BACKUP_ROOT="/srv/ss-pf-backups"
BACKUP_TIME=`date +%Y%m%d-%H%M%S`
BACKUP_PATH="$BACKUP_ROOT/$BACKUP_TIME"
echo "Creating backups in $BACKUP_PATH ..."
mkdir -p $BACKUP_PATH

# this assumes the pointer files are stored in the default location
# /var/archivematica/storage_service
# ( will exclude tmp and staging dirs )
tar -zc -f $BACKUP_PATH/pointer_files.tgz --directory /var/archivematica/storage_service --exclude="tmp*" --exclude="var" --exclude="recover" .
