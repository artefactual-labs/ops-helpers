#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Upload DIP to AtoM from command line.

This is intended to be run on the same server where archivematica
is running (i.e., archivematica user has ssh access to the AtoM
server so that rsyncing the DIP works)

Run as user archivematica:
$ sudo -u archivematica ./upload-dip-to-atom.py <source_dip> <atom_server_url> <atom_email> <atom_user_password> <rsync_target> <uuid>
"""

from __future__ import print_function
import argparse
import getpass
import os
import requests
import shlex
import subprocess
import sys

user = getpass.getuser()
if (user != 'archivematica'):
    print("Error: user is {}, run script with user archivematica (sudo -u archivematica)".format(user))
    sys.exit()

PREFIX = "[uploadDIP]"
# Print to stderr and exit
def error(message, code=1):
    print >>sys.stderr, "%s %s" % (PREFIX, message)
    sys.exit(1)

def upload_dip_to_atom():

    dip_directory = "/var/archivematica/sharedDirectory/www/DIPsStore/09c5/81e8/87cf/4cd1/979b/efff/e8d9/26cd/testdip2-7cc271e7-82f8-4e9d-aee4-4c8337d10b6f"
    rsync_target = "192.168.168.193:/tmp/"
    data_url = "http://192.168.168.193/index.php"
    target = "dipupload1"
    data_version = "2"
    data_email = "amdipupload@example.com"
    data_password = "amdipupload" 

    ############################# 
    # 1) rsync DIP to AtoM server
    #############################

    command_string = "rsync --protect-args -rltz -P --chmod=ugo=rwX {} {}".format(dip_directory, rsync_target)
    print ("will execute: {}".format(command_string))

    p = subprocess.Popen(shlex.split(command_string),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         )

    output = p.communicate()
    if p.returncode == 0:
        print('Successfully rsynced DIP')
        print('\n'.join(output))
    else:
        print('Failed to rsync DIP')
        print('\n'.join(output))

    ###############################
    # 2) sword API deposit request 
    ###############################

    # Building headers dictionary for the deposit request
    headers = {}
    headers['User-Agent'] = 'Archivematica'
    headers['X-Packaging'] = 'http://purl.org/net/sword-types/METSArchivematicaDIP'
    headers['Content-Type'] = 'application/zip'
    headers['X-No-Op'] = 'false'
    headers['X-Verbose'] = 'false'
    headers['Content-Location'] = "file:///{}".format(os.path.basename(dip_directory))

    # Build URL (expected sth like http://localhost/ica-atom/index.php)
    atom_url_prefix = ';' if data_version == 1 else ''
    data_url = "{}/{}sword/deposit/{}".format(data_url, atom_url_prefix, target)

    # Auth and request!
    print("About to deposit to: %s" % data_url)
    auth = requests.auth.HTTPBasicAuth(data_email, data_password)

    # Disable redirects: AtoM returns 302 instead of 202, but Location header field is valid
    response = requests.request('POST', data_url, auth=auth, headers=headers, allow_redirects=False)

    # response.{content,headers,status_code}
    print("> Response code: %s" % response.status_code)
    print("> Location: %s" % response.headers.get('Location'))

    print("> Content received: %s" % response.content)

    # Check AtoM response status code
    if response.status_code not in [200, 201, 302]:
        error("Response code not expected")

    # Location is a must, if it is not included in the AtoM response something was wrong
    if response.headers['Location'] is None:
        error("Location is expected, if not is likely something is wrong with AtoM")

    # (A)synchronously?
    if response.status_code == 302:
        print("Deposited asynchronously, AtoM is processing the DIP in the job queue")
    else:
        print("Deposited synchronously")


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='index AIP from aipstore.')
    #parser.add_argument('uuid', help='AIP UUID.')
    #args = parser.parse_args()

    #sys.exit(upload_dip_to_atom(args.uuid))
    sys.exit(upload_dip_to_atom())
