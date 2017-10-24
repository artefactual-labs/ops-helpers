#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Move an AIP between locations. This script is a temporary workaround,
until SSPR #143 is merged.
Use the python interpreter of the storage service virtualenv.
Run with user archivematica.
"""

from __future__ import print_function
import argparse
from lxml import etree
import getpass
import os
import shutil
import sys
import tempfile

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
from locations.models.location import Location
from locations.models.package import Package
from common import utils


# code borrowed from sspr 143
def move_to_location(package, destination_location_uuid):
    """
    Move a package to another location (that has the same purpose as package's current location).
    """
    destination_location = Location.active.get(uuid=destination_location_uuid)

    if package.current_location == destination_location:
        return

    if package.current_location.purpose != destination_location.purpose:
        raise ValueError('Location purpose mismatch for location %s' % destination_location_uuid)

    try:
        # Move to internal storage
        ss_internal = Location.active.get(purpose=Location.STORAGE_SERVICE_INTERNAL)
        # create temp directory
        temp_dir = tempfile.mkdtemp(prefix='movetmp', dir=destination_location.space.staging_path)
        temp_dir_basename = os.path.basename(os.path.normpath(temp_dir))

        source_path = os.path.join(
            package.current_location.relative_path,
            package.current_path)

        origin_space = package.current_location.space
        origin_space.move_to_storage_service(
            source_path=source_path,
            destination_path=temp_dir_basename,
            destination_space=destination_location.space)
        origin_space.post_move_to_storage_service()

        # Move to destination location
        source_path = os.path.join(
            temp_dir_basename,
            os.path.basename(package.current_path))
        destination_path = os.path.join(
            destination_location.relative_path,
            package.current_path)

        destination_space = destination_location.space
        destination_space.move_from_storage_service(
            source_path=source_path,
            destination_path=destination_path)
        destination_space.post_move_from_storage_service(
            staging_path=source_path,
            destination_path=destination_path,
            package=package)

        # delete temp directory
        shutil.rmtree(temp_dir)

        # Update location
        package.current_location = destination_location
        package.status = Package.UPLOADED
        package.save()
        package.current_location.space.update_package_status(package)

        # Update pointer file's location information
        if package.pointer_file_path and package.package_type in (Package.AIP, Package.AIC):
            root = etree.parse(package.full_pointer_file_path)
            element = root.find('.//mets:file', namespaces=utils.NSMAP)
            flocat = element.find('mets:FLocat', namespaces=utils.NSMAP)
            if package.uuid in element.get('ID', '') and flocat is not None:
                # TODO: use PREFIX_NS in later version
                flocat.set('{{{ns}}}href'.format(ns=utils.NSMAP['xlink']), package.full_path)
            # Add USE="Archival Information Package" to fileGrp.  Required for
            # LOCKSS, and not provided in Archivematica <=1.1
            if root.find('.//mets:fileGrp[@USE="Archival Information Package"]', namespaces=utils.NSMAP) is None:
                root.find('.//mets:fileGrp', namespaces=utils.NSMAP).set('USE', 'Archival Information Package')

            with open(package.full_pointer_file_path, 'w') as f:
                f.write(etree.tostring(root, pretty_print=True))

    except Exception:
        print('Attempt to move package %s to location %s failed', package.uuid, destination_location_uuid, exc_info=True)


def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('aip_uuid', help="UUID of the AIP to move")
    parser.add_argument('destloc_uuid', help="UUID of the destination location")
    args = parser.parse_args(arguments)

    # verify that AIP exists
    pac = Package.objects.get(uuid=args.aip_uuid)
    print(pac)

    # verify that location exists
    loc = Location.objects.get(uuid=args.destloc_uuid)
    print(loc)

    # call function to move package to new location
    move_to_location(pac, args.destloc_uuid)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
