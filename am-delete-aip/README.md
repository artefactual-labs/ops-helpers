## am-delete-aip

### delete-aip-request.py

Sends an AIP delete request to the Storage Service. Useful when the AIP that needs to be deleted is not in the Dashboard's Archival Storage. 

This script is a temporary workaround, currently there is no way to delete an AIP from the storage service database if the AIP is not in listed in Archival Storage.

```
$ /usr/share/python/archivematica-dashboard/bin/python delete-aip-request.py amuser 874d1f31-f11c-4bad-8072-8260b9d07e12 "test deletion of package"
parameters: amuser 874d1f31-f11c-4bad-8072-8260b9d07e12 test deletion of package
user amuser 1 user@example.com
Delete request created successfully.
```

Note: Do not use if the AIP is listed in the Dashboard's Archival Storage (the AIP will still show there as stored)


### ss-delete-dip.py

Delete a DIP from the Storage Service database.
Use the python interpreter of the storage service virtualenv.
Run with user archivematica.

```
$ sudo -u archivematica /usr/share/python/archivematica-storage-service/bin/python ss-
delete-dip.py 8ebf7952-d767-4e63-8082-372ab2addea0
8ebf7952-d767-4e63-8082-372ab2addea0: /var/archivematica/sharedDirectory/www/DIPsStore/8ebf/7952/d767/4e63/8082/372a/b2ad/dea0/test1-662d4202
-246e-4b38-bf67-8a6049b3e7d9
deleted: 8ebf7952-d767-4e63-8082-372ab2addea0
```