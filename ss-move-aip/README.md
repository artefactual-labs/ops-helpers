## ss-move-aip

Move AIP between locations, based on SSPR #143.
This script is a temporary workaround, until SSPR #143 is merged.
Use the python interpreter of the storage service virtualenv.
Run with user archivematica.

Example: move AIP UUID 662d4202-246e-4b38-bf67-8a6049b3e7d9 to location whose UUID is 219cf60f-ed1d-46e5-b8ba-f167e4899f10:

```
$ sudo -u archivematica /usr/share/python/archivematica-storage-service/bin/python ss-move-aip.py 662d4202-246e-4b38-bf67-8a6049b3e7d9 219cf60f-ed1d-46e5-b8ba-f167e4899f10
662d4202-246e-4b38-bf67-8a6049b3e7d9: /mnt/aipstore2/662d/4202/246e/4b38/bf67/8a60/49b3/e7d9/test1-662d4202-246e-4b38-bf67-8a6049b3e7d9.7z
219cf60f-ed1d-46e5-b8ba-f167e4899f10: mnt/aipstore1 (AIP Storage)
```

