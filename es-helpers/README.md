<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [es-helpers](#es-helpers)
  - [es-repo.py (snapshots and repositories)](#es-repopy-snapshots-and-repositories)
    - [Create a elasticsearch repository:](#create-a-elasticsearch-repository)
    - [List repositories:](#list-repositories)
    - [Create snapshot](#create-snapshot)
    - [Get snapshot information](#get-snapshot-information)
    - [Restore snapshot](#restore-snapshot)
  - [es-scan.py (scan)](#es-scanpy-scan)
    - [scan_count](#scan_count)
    - [scan_show](#scan_show)
    - [scan_del](#scan_del)
  - [es-reindex.sh (update search indices)](#es-reindexsh-update-search-indices)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# es-helpers

Scripts to help elasticsearch sysadmin work. Uses elasticsearch-py.

## es-repo.py (snapshots and repositories)

### Create a elasticsearch repository:

```
$ python es-repo.py createrepo --reponame repo1 --repopath /var/lib/elasticsearch/backup-repo-1
{u'acknowledged': True}

$ python es-repo.py createrepo --reponame repo2 --repopath /var/lib/elasticsearch/backup-repo-2 {u'acknowledged': True}
```


### List repositories:

```
$ python es-repo.py getrepos
{u'repo1': {u'settings': {u'location': u'/var/lib/elasticsearch/backup-repo-1'},
            u'type': u'fs'},
 u'repo2': {u'settings': {u'location': u'/var/lib/elasticsearch/backup-repo-2'},
            u'type': u'fs'}}
```


### Create snapshot

```
$ python es-repo.py createsnap --reponame repo1 --snapname
 snapshot2 --indices aips
{u'snapshot': {u'duration_in_millis': 102,
               u'end_time': u'2015-09-15T20:24:54.305Z',
               u'end_time_in_millis': 1442348694305,
               u'failures': [],
               u'indices': [u'aips'],
               u'shards': {u'failed': 0, u'successful': 5, u'total': 5},
               u'snapshot': u'snapshot2',
               u'start_time': u'2015-09-15T20:24:54.203Z',
               u'start_time_in_millis': 1442348694203,
               u'state': u'SUCCESS'}}
```


### Get snapshot information

```
$ python es-repo.py getsnap --reponame repo1 --snapname snapshot2
{u'snapshots': [{u'duration_in_millis': 102,
                 u'end_time': u'2015-09-15T20:24:54.305Z',
                 u'end_time_in_millis': 1442348694305,
                 u'failures': [],
                 u'indices': [u'aips'],
                 u'shards': {u'failed': 0, u'successful': 5, u'total': 5},
                 u'snapshot': u'snapshot2',
                 u'start_time': u'2015-09-15T20:24:54.203Z',
                 u'start_time_in_millis': 1442348694203,
                 u'state': u'SUCCESS'}]}
```

```
$ python es-repo.py getsnap --reponame repo1
{u'snapshots': [{u'duration_in_millis': 35,
                 u'end_time': u'2015-09-15T20:24:30.376Z',
                 u'end_time_in_millis': 1442348670376,
                 u'failures': [],
                 u'indices': [],
                 u'shards': {u'failed': 0, u'successful': 0, u'total': 0},
                 u'snapshot': u'snapshot1',
                 u'start_time': u'2015-09-15T20:24:30.341Z',
                 u'start_time_in_millis': 1442348670341,
                 u'state': u'SUCCESS'},
                {u'duration_in_millis': 102,
                 u'end_time': u'2015-09-15T20:24:54.305Z',
                 u'end_time_in_millis': 1442348694305,
                 u'failures': [],
                 u'indices': [u'aips'],
                 u'shards': {u'failed': 0, u'successful': 5, u'total': 5},
                 u'snapshot': u'snapshot2',
                 u'start_time': u'2015-09-15T20:24:54.203Z',
                 u'start_time_in_millis': 1442348694203,
                 u'state': u'SUCCESS'}]}
```

### Restore snapshot

```
$ python es-repo.py restore --reponame repo1 --snapname snapshot2 --index aips --target aipsrestoretest2
{u'snapshot': {u'indices': [u'aipsrestoretest2'],
               u'shards': {u'failed': 0, u'successful': 5, u'total': 5},
               u'snapshot': u'snapshot2'}}
```

## es-scan.py (scan)

### scan_count

Scan ES index `transfers` for backlog entries (`status:backlog`) and show count (number of items):

```
$ python es-scan.py scan_count -i transfers  -q '{"query": {"match": {"status": "backlog"}}}'
1945
```

### scan_show

Scan ES index `transfers` for backlog entries and print the entries:

```
$ python es-scan.py scan_show -i transfers  -q '{"query": {"match": {"status": "backlog"}}}'
...
...
{u'_score': 0.0, u'_type': u'transferfile', u'_id': u'AVms3OUfHYlZdVHpuf8w', u'_source': {u'accessionid': u'2012-090', u'status': u'backlog', u'sipuuid': u'b1b60f4e-a336-4184-9c66-8a406ae92e50', u'created': 1484663862.353921, u'file_extension': u'jpg', u'filename': u'txsau_ms00418_00674.jpg', u'ingestdate': u'2017-01-17', u'relative_path': u'MarquisePhotosmd-b1b60f4e-a336-4184-9c66-8a406ae92e50/objects/Pride_Picnic_1994/jpegs/txsau_ms00418_00674.jpg', u'fileuuid': u'e92ef9ba-2836-4739-aa37-f0b5bb747e18', u'origin': u'6be772ad-b0d0-4271-9602-6a3f98ecada1'}, u'_index': u'transfers'}
{u'_score': 0.0, u'_type': u'transferfile', u'_id': u'AVms3OWoHYlZdVHpuf82', u'_source': {u'accessionid': u'2012-090', u'status': u'backlog', u'sipuuid': u'b1b60f4e-a336-4184-9c66-8a406ae92e50', u'created': 1484663862.353921, u'file_extension': u'log', u'filename': u'filenameCleanup.log', u'ingestdate': u'2017-01-17', u'relative_path': u'MarquisePhotosmd-b1b60f4e-a336-4184-9c66-8a406ae92e50/logs/filenameCleanup.log', u'fileuuid': u'', u'origin': u'6be772ad-b0d0-4271-9602-6a3f98ecada1'}, u'_index': u'transfers'}
```

### scan_del

Scan ES index `transfers` for backlog entries and delete the entries from the index:

```
$ python es-scan.py scan_del -i transfers  -q '{"query": {"match": {"status": "backlog"}}}'
...
...
{u'found': True, u'_type': u'transferfile', u'_id': u'AVms3OUfHYlZdVHpuf8w', u'_version': 3, u'_index': u'transfers'}
{u'found': True, u'_type': u'transferfile', u'_id': u'AVms3OWoHYlZdVHpuf82', u'_version': 3, u'_index': u'transfers'}

( checking for backlog items after deletion)
$ python es-scan.py scan_count -i transfers  -q '{"query": {"match": {"status": "backlog"}}}'
0
```

## es-reindex.sh (update search indices)

Apply the search document mappings found in Archivematica releases to existing
documents using the [Reindex API]. This is the fastest method to update
Archivematica search indices when upgrading the software and should guarantee
a working Archivematica installation, but it will not populate the contents of
new fields introduced in the new release.

Before using this script, please back up your search indices. The script
assumes that the cluster is reachable via `127.0.0.1:9200` but the `es_url`
variable can be adjusted as needed.

Ensure that the Elasticsearch heap size is big enough to accomodate the size
of the indices. The size can be adjusted in `/etc/default/elasticsearch`
(Ubuntu) or `/etc/sysconfig/elasticsearch` (CentOS).

    $ grep ES_JAVA_OPTS= /etc/default/elasticsearch
    ES_JAVA_OPTS="-Xms2g -Xmx2g"

To find the right value, it is possible to guess the total size by listing
all search indices. E.g. assuming that the search cluster is available via
`127.0.0.1:9200`, try running the following command:

    $ curl -s -X GET 'http://localhost:9200/_cat/indices/%2A?v=&s=index:desc'
    health status index         uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    yellow open   transfers     lYqkYjwZRy2XG8CP_3S3PQ   5   1          0            0      1.2kb          1.2kb
    yellow open   transferfiles K5gnDZyOQz2JdIeZ6adJsQ   5   1          0            0      1.2kb          1.2kb
    yellow open   aips          yAyK_koXThaZcWsBYfzN7w   5   1         17            0    101.4mb        101.4mb
    yellow open   aipfiles      TVrrX8jkRhWWxGfvK_M6zg   5   1      11987            0      2.9gb          2.9gb

In the example above, we'd use:

    ES_JAVA_OPTS="-Xms3g -Xmx3g"

To run the script, please just download `es-reindex.sh` in the Archivematica
server and run the script with a user with sudo privileges. For instance:

```
wget https://raw.githubusercontent.com/artefactual-labs/ops-helpers/master/es-helpers/es-reindex.sh

chmod +x es-reindex.sh

./es-reindex.sh
```

In our example, this script took 11 minutes to complete. If it fails, try
checking out the logs (`/var/log/elasticsearch.log`). Most likely, the JVM
heap size ran out of memory. You can start over by restoring your back up or
putting back the old indices.

More details can be found in the Archivematica [upgrading docs].

[Reindex API]: https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html
[upgrading docs]: https://www.archivematica.org/es/docs/latest/admin-manual/installation-setup/upgrading/upgrading/
