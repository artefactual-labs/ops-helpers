#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Delete a DIP from the Storage Service database.
Use the python interpreter of the storage service virtualenv.
Run with user archivematica.
"""

from __future__ import print_function
import argparse
import getpass
import os
import sys

user = getpass.getuser()
if (user != 'archivematica'):
    print("Error: user is {}, run script with user archivematica (sudo -u archivematica)".format(user))
    sys.exit()

sys.path.append('/usr/lib/archivematica/storage-service')
os.environ['DJANGO_SETTINGS_MODULE'] = 'storage_service.settings.production'
os.environ['DJANGO_SECRET_KEY'] = 'dummy'
os.environ['SS_DB_NAME'] = '/var/archivematica/storage-service/storage.db'
os.environ['SS_DB_USER'] = 'dummy'
os.environ['SS_DB_PASSWORD'] = 'dummy'
os.environ['SS_DB_HOST'] = 'dummy'

import django
django.setup()
from locations.models.package import Package


def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dip_uuid', help="UUID of the DIP to delete")
    args = parser.parse_args(arguments)

    # verify that DIP exists
    pac = Package.objects.get(uuid=args.dip_uuid, package_type="DIP")
    print(pac)

    # delete corresponding Package object
    pac.delete()
    print ("deleted: {}".format(args.dip_uuid))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
