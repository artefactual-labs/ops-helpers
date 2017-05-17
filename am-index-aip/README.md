<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [am-index-aip](#am-index-aip)
  - [Use case example for batch indexing of many AIPs](#use-case-example-for-batch-indexing-of-many-aips)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## am-index-aip

Add AIP to the dashboard index (Archival Storage tab) of an 
archivematica instance. AIP is specified by UUID.

This script connects to the Storage Service associated with
the archivematica dashboard instance, downloads the AIP,
and then uses the MCPclient script indexAIP.py for indexing.


Run as user archivematica, use the python interpreter of the MCP client virtualenv (if using a separate one):
```bash
$ sudo -u archivematica /usr/share/python/archivematica-mcp-client/bin/python index-aip-from-aipstore.py <aip_uuid>
```
If not using a separate virtualenv for MCP Client:
```
$ sudo -u archivematica ./index-aip-from-aipstore.py <aip_uuid>
```

### Use case example for batch indexing of many AIPs

For example, to index all the AIPs belonging to a specified pipeline dashboard UUID: 818c6978-aa69-4ab9-90ca-7c1a445b5a78

1. Get the list of AIP uuids from the Storage Service database:

```bash
$ sqlite3 /var/archivematica/storage-service/storage.db 'select uuid from locations_package where origin_pipeline_id="818c6978-aa69-4ab9-90ca-7c1a445b5a78" and package_type="AIP" and status="UPLOADED";' > aips-to-reindex.txt
```

2. Use a loop to iterate over the uuids:

```bash
$ cat aips-to-reindex.txt | while read line; do  sudo -u archivematica /usr/share/python/archivematica-mcp-client/bin/python index-aip-from-aipstore.py "$line"; done
```

The [`script` command](https://linux.die.net/man/1/script) can be used to save the output to a file.