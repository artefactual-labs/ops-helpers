#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Show human readable messages for a specified processingMCP file
It uses the Django ORM to match the uuids in the file to the
corresponding entries in the related Dashboard models
(MicroServiceChainLink, etc)

Use the python interpreter of the MCP dashboard virtualenv:
$ /usr/share/python/archivematica-dashboard/bin/python am-chains-decode-procmcp.py <processingMCPfile.xml>
"""
from __future__ import print_function
import argparse
import os
import sys
import xml.etree.ElementTree as ET

sys.path.append('/usr/lib/archivematica/archivematicaCommon')
sys.path.append('/usr/share/archivematica/dashboard')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.common'

from main.models import MicroServiceChainLink, MicroServiceChain, MicroServiceChoiceReplacementDic


def decode_proc_mcp(proc_mcp_filename):

    # read proc MCP file, add chains file text if found
    tree = ET.parse(proc_mcp_filename)
    root = tree.getroot()
    for choice in root[0]:
        appto = choice.find('appliesTo').text
        gotoch = choice.find('goToChain').text

        print('appliesTo: {}'.format(appto))
        print('goToChain: {}'.format(gotoch))

        # find the matching chainlink for appliesTo entry
        try:
            chainlink = MicroServiceChainLink.objects.get(id=appto)
            print ("appliesTo (MicroServiceChainLink): {}".format(chainlink.currenttask.description))
        except MicroServiceChainLink.MultipleObjectsReturned:
            print ("appliesTo (MicroServiceChainLink) error: MultipleObjectsReturned")
        except MicroServiceChainLink.DoesNotExist:
            print ("appliesTo (MicroServiceChainLink) error: DoesNotExist")
        except:
            print ("appliesTo (MicroServiceChainLink) error: Unexpected error")

        # find the matching chain for gotoChain entry in MicroServiceChain
        try:
            chain = MicroServiceChain.objects.get(id=gotoch)
            print ("goToChain (MicroServiceChain): {}".format(chain.description))
        except MicroServiceChain.MultipleObjectsReturned:
            print ("goToChain (MicroServiceChain) error: MultipleObjectsReturned")
        except MicroServiceChain.DoesNotExist:
            print ("goToChain (MicroServiceChain) not found, looking in MicroServiceChoiceReplacementtDic...")
            # find the matching chain for gotoChain entry in MicroServiceChoiceReplacementDic
            try:
                chain = MicroServiceChoiceReplacementDic.objects.get(id=gotoch)
                print ("goToChain (MicroServiceChoiceReplacementtDic): {}".format(chain.description))
            except MicroServiceChoiceReplacementDic.MultipleObjectsReturned:
                print ("goToChain (MicroServiceChoiceReplacementtDic) error: MultipleObjectsReturned")
            except MicroServiceChoiceReplacementDic.DoesNotExist:
                print ("goToChain (MicroServiceChoiceReplacementtDic) error: DoesNotExist")
            except:
                print ("goToChain (MicroServiceChoiceReplacementtDic) error: Unexpected error")
        except:
            print ("goToChain (MicroServiceChain) error: Unexpected error")

        print('----')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parse processing MCP file')
    parser.add_argument('proc_mcp_filename', help='processing MCP file')
    args = parser.parse_args()

    sys.exit(decode_proc_mcp(args.proc_mcp_filename))
