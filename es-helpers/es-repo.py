# elasticsearch repository helper script

import argparse
from elasticsearch import Elasticsearch, Urllib3HttpConnection
import sys
import pprint

ES_TIMEOUT = 3600


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', type=str, default='127.0.0.1:9200')
    subparsers = parser.add_subparsers(help='sub-command help')

    # createrepo command
    parser_createrepo =  subparsers.add_parser('createrepo', help='create snapshot repo')
    parser_createrepo.add_argument('--reponame', type=str, required=True)
    parser_createrepo.add_argument('--repopath', type=str, required=True)
    parser_createrepo.set_defaults(func=createrepo)

    # getrepos command
    parser_listrepo = subparsers.add_parser('getrepos', help='list repos')
    parser_listrepo.set_defaults(func=getrepos)

    # createsnap command
    parser_createsnap = subparsers.add_parser('createsnap', help='create snapshot')
    parser_createsnap.add_argument('--reponame', help="repository name", type=str, required=True)
    parser_createsnap.add_argument('--snapname', help="snapshot name", type=str, required=True)
    parser_createsnap.add_argument('--indices', help="indices to be snapshotted", type=str, required=True)
    parser_createsnap.set_defaults(func=createsnap)

    # getsnap command
    parser_getsnap = subparsers.add_parser('getsnap', help='get snapshot information')
    parser_getsnap.add_argument('--reponame', help="repository name", type=str, required=True)
    parser_getsnap.add_argument('--snapname', help="snapshot name(s)", type=str, required=False)
    parser_getsnap.set_defaults(func=getsnap)

    # restore command
    parser_restore = subparsers.add_parser('restore', help='restore snapshot index from repository')
    parser_restore.add_argument('--reponame', help="repository name", type=str, required=True)
    parser_restore.add_argument('--snapname', help="snapshot name", type=str, required=True)
    parser_restore.add_argument('--index', help="source index name", type=str, required=True)
    parser_restore.add_argument('--target', help="target index name", type=str, required=True)
    parser_restore.set_defaults(func=restore)


    # parse arguments
    args = parser.parse_args()
    return args


def createrepo(ss, args):
    repository_settings = {
        'type': 'fs',
        'settings': {
            'location': args.repopath,
        },
    }
    r = ss.create_repository(repository=args.reponame, body=repository_settings)
    pprint.pprint(r)
    return

def getrepos(ss, args):
    r = ss.get_repository()
    pprint.pprint(r)
    return

def createsnap(ss, args):
    r = ss.create(repository=args.reponame,
                  snapshot=args.snapname,
                  wait_for_completion=True,
                  body={'indices': args.indices})
    pprint.pprint(r)
    return

def getsnap(ss, args):
    if args.snapname:
        r = ss.get(repository=args.reponame,
                   snapshot=args.snapname)
    else:
        r = ss.get(repository=args.reponame,
                   snapshot="_all")
    pprint.pprint(r)
    return

def restore(ss, args):
    r = ss.restore(repository=args.reponame,
                   snapshot=args.snapname,
                   wait_for_completion=True,
                   body={ 'indices': args.index,
                          'rename_pattern': args.index,
                          'rename_replacement': args.target,
                         })
    pprint.pprint(r)
    return

def main():

    args = parse_arguments()

    es = Elasticsearch(args.server, connection_class=Urllib3HttpConnection, timeout=ES_TIMEOUT)
    ss = es.snapshot
    args.func(ss, args)


if __name__ == '__main__':
    sys.exit(main())


