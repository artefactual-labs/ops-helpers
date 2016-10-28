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

