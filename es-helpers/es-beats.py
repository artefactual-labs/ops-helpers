#!/usr/bin/env python3
"""
es-beats: helper for ES beats stuff
Uses elasticsearch-py (tested with ES 5, elasticsearch-py v5.4)

"""
__author__ = "Artefactual Systems"
__version__ = "0.1.0"
__license__ = "AGPLv3"

import argparse
import datetime
from elasticsearch import Elasticsearch, Urllib3HttpConnection


ES_TIMEOUT = 3600


def parse_arguments():
    # top level parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', type=str, default='127.0.0.1:9200')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

    # subparser for sub-command: list_ind 
    parser_list_ind = subparsers.add_parser('list_ind', help='list beats indices')
    parser_list_ind.set_defaults(func=list_ind)

    # subparser for sub-command: del_ind
    parser_del_ind = subparsers.add_parser('del_ind', help='delete old beats indices')
    parser_del_ind.add_argument('days', type=int, help='delete indices older than specified days')
    parser_del_ind.set_defaults(func=del_ind)

    # parse arguments
    args = parser.parse_args()
    return args


def list_ind(args, es):
    # list beats indices (filebeat and metricbeat)
    l = es.indices.get_alias(["filebeat-*", "metricbeat-*"])
    for i in l:
        print(i)
    return


def del_ind(args, es):
    print ("Deleting beats indices more than {} days old".format(args.days))
    # not sure if indices created by UTC date, but will use UTC for now
    # get today's UTC date
    now = datetime.datetime.utcnow()
    print("today is {}".format(now.day))

    return


def main():
    args = parse_arguments()
    es = Elasticsearch(args.server, connection_class=Urllib3HttpConnection, timeout=ES_TIMEOUT)
    # print(args)
    # execute sub-command if specified in command line
    if args.subparser_name:
        args.func(args, es)


if __name__ == "__main__":
    main()
