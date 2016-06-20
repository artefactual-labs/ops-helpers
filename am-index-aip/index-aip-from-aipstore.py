#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Add AIP to the dashboard index (Archival Storage tab) of an 
archivematica instance. AIP is specified by UUID.

This script connects to the Storage Service associated with
the archivematica dashboard instance, downloads the AIP,
and then uses the MCPclient script indexAIP.py for indexing.

Run as user archivematica:
$ sudo -u archivematica ./index-aip-from-aipstore.py <aip_uuid>
"""

from __future__ import print_function
import argparse
import getpass
import glob
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import urllib

user = getpass.getuser()
if (user != 'archivematica'):
    print("Error: user is {}, run script with user archivematica (sudo -u archivematica)".format(user))
    sys.exit()

sys.path.append('/usr/lib/archivematica/archivematicaCommon')
sys.path.append('/usr/share/archivematica/dashboard')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.common'

import django
django.setup()
import storageService as storage_service

TMP_DIR_BASE = '/var/archivematica/sharedDirectory/tmp'


def index_from_aipstore(uuid):

    # check if uuid exists in the AIPstore
    file_info = storage_service.get_file_info(uuid=uuid)
    if len(file_info) != 1:
        print("Error: number of packages returned from aipstore: {}. Must be 1".format(len(file_info)))
        return -1
    # check if package_type is "AIP""
    print("file info: {}".format(file_info))
    if file_info[0]['package_type'] != 'AIP':
        print("Error: package is not AIP: {}".format(file_info[0]['package_type']))
        return -2

    # get AIP file name from file info
    basename = os.path.basename(file_info[0]['current_path'])
    filename, file_extension = os.path.splitext(basename)

    # get aip download url
    aip_download_url = storage_service.download_file_url(file_uuid=uuid)
    print("AIP download URL: {}".format(aip_download_url))

    # create a temp directory for processing
    tempdir = tempfile.mkdtemp(prefix='aiptmp', dir=TMP_DIR_BASE)
    print("Created: {}".format(tempdir))

    # download file to temp directory
    urllib.urlretrieve(aip_download_url, os.path.join(tempdir, basename))
    print("aip downloaded to directory")

    # expand aip files
    command_string = "atool --extract-to=. {}".format(basename)
    print ("will execute: {}".format(command_string))
    p = subprocess.Popen(shlex.split(command_string),
                         cwd=tempdir,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                    )
                    
    output = p.communicate()
    if p.returncode == 0:
        print('Successfully extracted AIP')
        print('\n'.join(output))
    else:
        print('Failed to extract AIP')
        print('\n'.join(output))

    # delete downloaded file now that we have it expanded
    os.remove(os.path.join(tempdir, basename))

    # get aip path to pass to the client script
    dirlist = glob.glob(os.path.join(tempdir, "*"))
    if (len(dirlist) != 1):
        print("Error: {} must have only one directory".format(tempdir))
        return -4
    if (not os.path.isdir(dirlist[0])):
        print("Error: {} must be a directory".format(dirlist[0]))
        return -4
    
    # populate the 4 variables needed to call the aip index script
    sip_uuid=uuid
    sip_name=filename[:-37]     # strip uuid and dashes
    sip_path = os.path.join(dirlist[0],"data")  # METS etc inside the data/ directory of the AIP
    sip_type="REIN"     # setting as reingest so that existing index entries are removed beforehand 

    command_string = "./indexAIP.py {} {} {} {}".format(sip_uuid, sip_name, sip_path, sip_type)
    print ("will execute: {}".format(command_string))


    p = subprocess.Popen(shlex.split(command_string),
                         cwd="/usr/lib/archivematica/MCPClient/clientScripts",
                         env={"DJANGO_SETTINGS_MODULE": "settings.common", 
                              "PYTHONPATH": "/usr/share/archivematica/dashboard:/usr/lib/archivematica/archivematicaCommon" },
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                    )
                    
    output = p.communicate()
    if p.returncode == 0:
        print('Successfully indexed AIP {0}'.format(sip_uuid))
        print('\n'.join(output))
    else:
        print('Failed to index AIP {0}'.format(sip_uuid))
        print('\n'.join(output))

    # delete temporary processing directory
    shutil.rmtree(tempdir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='index AIP from aipstore.')
    parser.add_argument('uuid', help='AIP UUID.')
    args = parser.parse_args()

    sys.exit(index_from_aipstore(args.uuid))
