#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Sends an AIP delete request. This script is a temporary workaround,
currently there is no way to delete an AIP from the storage service
database if the AIP is not in listed in Archival Storage.

Use the python interpreter of the dashboard virtualenv:
$ /usr/share/python/archivematica-dashboard/bin/python delete-aip-request.py <args>

Note: Do not use if the AIP is listed in the Dashboard's Archival
Storage (the AIP will still show there as stored)
"""

from __future__ import print_function
import argparse
import os
import sys

sys.path.append('/usr/lib/archivematica/archivematicaCommon')
sys.path.append('/usr/share/archivematica/dashboard')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.common'

import storageService as storage_service
from django.contrib.auth.models import User


def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument('conffile', help="Config file")
    parser.add_argument('username', help="dashboard username")
    parser.add_argument('uuid', help="AIP uuid to delete")
    parser.add_argument('reason', help="reason for deletion")
    args = parser.parse_args(arguments)

    print("parameters: {} {} {}".format(args.username, args.uuid, args.reason))
    # # parse config file
    # parse_config_file(args.conffile)

    # get the user_id and user_email from the MCP database
    user = User.objects.get(username=args.username)
    print("user {} {} {}".format(args.username, user.id, user.email))

    # send delete AIP request
    response = storage_service.request_file_deletion(args.uuid, user.id, user.email, args.reason)
    print(response['message'])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
