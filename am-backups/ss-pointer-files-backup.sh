#!/bin/bash

# - If some files are not readable the script will output error messages
# - To ensure that all the pointer files are readable by the user
#   running this script, do for example:
#   $ sudo chmod -R o+Xr /var/archivematica/storage_service 

# Change BACKUP_ROOT as needed to save backup to a different directory
BACKUP_ROOT="/var/artefactual/ss-pf-backups"
BACKUP_TIME=`date +%Y%m%d-%H%M%S`
BACKUP_PATH="$BACKUP_ROOT/$BACKUP_TIME"
echo "Creating backups in $BACKUP_PATH ..."
mkdir -p $BACKUP_PATH

# Change SS_PF_LOCATION if the pointer files are not stored in the
# default location (/var/archivematica/storage_service)
SS_PF_LOCATION="/var/archivematica/storage_service"

# Pointer files path/name examples:
# - Some include the uuid in the filename:
#   cf54/4804/... /pointer.cf544804-d022-4be8-b1b7-9299e0d040aa.xml
# - Some just named pointer.xml:
#   69b1/82d0/... /pointer.xml
# (depending on the AM version they were created?)

# (ref. https://superuser.com/questions/513304/how-to-combine-the-tar-command-with-find/513319#513319)
# - the "-printf %P\\0" %P option removes the starting point
#   directory ($SS_PF_LOCATION) from the file path,
#   \0 adds an ASCII null at the end (double backlash to escape to
#   avoid shell substitution)

find $SS_PF_LOCATION -type f -iname "pointer*xml" -printf %P\\0 | tar -rf $BACKUP_PATH/pointer_files.tar --directory $SS_PF_LOCATION --null -T -
gzip $BACKUP_PATH/pointer_files.tar

