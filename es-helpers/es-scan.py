# elasticsearch-py scan helper function

from __future__ import print_function

import argparse
from elasticsearch import Elasticsearch, Urllib3HttpConnection, helpers
import json
import sys

ES_TIMEOUT = 3600


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', type=str, default='127.0.0.1:9200')
    subparsers = parser.add_subparsers(help='sub-command help')

    # scan_count command
    parser_scan_count = subparsers.add_parser('scan_count', help='scan index and count')
    parser_scan_count.add_argument('-i', '--index', type=str, required=True)
    parser_scan_count.add_argument('-q', '--query', type=str, required=True)
    parser_scan_count.set_defaults(func=scan_count)

    # scan_show command
    parser_scan_show = subparsers.add_parser('scan_show', help='scan index and show items')
    parser_scan_show.add_argument('-i', '--index', type=str, required=True)
    parser_scan_show.add_argument('-q', '--query', type=str, required=True)
    parser_scan_show.set_defaults(func=scan_show)

    # scan_del command
    parser_scan_del = subparsers.add_parser('scan_del', help='scan index and delete matched items in query')
    parser_scan_del.add_argument('-i', '--index', type=str, required=True)
    parser_scan_del.add_argument('-q', '--query', type=str, required=True)
    parser_scan_del.set_defaults(func=scan_del)

    # parse arguments
    args = parser.parse_args()
    return args


def scan_count(es, r):
    s = sum(1 for _ in r)
    print(s)
    return


def scan_show(es, r):
    for item in r:
        print(item)
    return


def scan_del(es, r):
    for item in r:
        d = es.delete(index=item[u'_index'],
                      doc_type=item[u'_type'],
                      id=item[u'_id'])
        print(d)
    return


def main():

    args = parse_arguments()

    es = Elasticsearch(args.server, connection_class=Urllib3HttpConnection, timeout=ES_TIMEOUT)
    r = helpers.scan(es,
                     index=args.index,
                     query=json.loads(args.query))
    args.func(es, r)


if __name__ == '__main__':
    sys.exit(main())
