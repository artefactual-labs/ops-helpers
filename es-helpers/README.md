<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [es-helpers](#es-helpers)
  - [Create a elasticsearch repository:](#create-a-elasticsearch-repository)
  - [List repositories:](#list-repositories)
  - [Create snapshot](#create-snapshot)
  - [Get snapshot information](#get-snapshot-information)
  - [Restore snapshot](#restore-snapshot)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## es-helpers

Scripts to help elasticsearch sysadmin work

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
