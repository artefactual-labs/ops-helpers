<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [am-index-aip](#am-index-aip)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## am-index-aip

Add AIP to the dashboard index (Archival Storage tab) of an 
archivematica instance. AIP is specified by UUID.

This script connects to the Storage Service associated with
the archivematica dashboard instance, downloads the AIP,
and then uses the MCPclient script indexAIP.py for indexing.

Run as user archivematica:
```
$ sudo -u archivematica ./index-aip-from-aipstore.py <aip_uuid>
```