# am-import-index-aips

The `am-import-index-aips.sh` script imports and adds to the ES indices AIPs from files.

## Download the script

Just download the script in the AM server:

```
cd /tmp
wget https://raw.githubusercontent.com/artefactual-labs/ops-helpers/master/am-import-index-aips/am-import-index-aips.sh -O /tmp/am-import-index-aips.sh
chmod +x /tmp/am-import-index-aips.sh
```

## Configure the script variables

Please change variables for your system in the `/tmp/am-import-index-aips.sh` file.

* `PIPELINE_UUID`: UUID of the pipeline for the imported (new) AIP.
* `AIP_STORE_LOCATION_UUID`: UUID of the AIP Store for the imported (new) AIP.
* `AIPS_FILES_LIST`: A list with the AIP files (or relative path, using `AIP_DIR` as base). One line for every AIP.
* `AIP_DIR`: Directory (or base directory) where the AIP files are located.
* `AIP_STORE_PATH`: Path of the AIP_STORE_LOCATION_UUID location (check the SS).
* `AM_CONFIG_DIR`: `/etc/default` on Ubuntu and `/etc/sysconfig` on CentOS.
* `AIP_TMP_DIR`: Temporary directory to save AIPs while processing the import.

For instance, if have the following 2 AIPs to be imported:

```
/mnt/aip-store/a7b6/6252/9f77/4765/8d8d/1366/9503/1687/ac29_AIP1_228-3769-a7b66252-9f77-4765-8d8d-136695031687.7z
/mnt/aip-store/0e32/556c/e38d/47b9/9a96/3d77/cbbe/d0a2/ac18_AIP2_3940-4758-0e32556c-e38d-47b9-9a96-3d77cbbed0a2.7z
```

You can use:

```
AIPS_FILES_LIST=aip_list.txt
AIP_DIR=/mnt/aip-store
```

With the `aip_list.txt` content:

```
a7b6/6252/9f77/4765/8d8d/1366/9503/1687/ac29_AIP1_228-3769-a7b66252-9f77-4765-8d8d-136695031687.7z
0e32/556c/e38d/47b9/9a96/3d77/cbbe/d0a2/ac18_AIP2_3940-4758-0e32556c-e38d-47b9-9a96-3d77cbbed0a2.7z
```

## Run script

Run with:

```
./am-import-index-aips.sh
```

**NOTE1**: The archivematica user must have permissions to read the AIPs from the `AIP_DIR`.
**NOTE2**: The archivematica user must have permissions to write on the `AIP_TMP_DIR` dir.
**NOTE3**: If you have an error when importing the AIP, please chechk the following issue and workaround:
	* https://github.com/archivematica/Issues/issues/1516
