#!/bin/bash
BACKUP_ROOT="/srv/ss-db-backups"
BACKUP_TIME=`date +%Y%m%d-%H%M%S`
BACKUP_PATH="$BACKUP_ROOT/$BACKUP_TIME"
echo "Creating backups in $BACKUP_PATH ..."
mkdir -p $BACKUP_PATH
# sqlite file
cp /var/archivematica/storage-service/storage.db $BACKUP_PATH/storage.db
# also do a sql dump
sqlite3 /var/archivematica/storage-service/storage.db .dump | gzip -c > $BACKUP_PATH/storage.sql.gz
