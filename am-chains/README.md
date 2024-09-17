# am-chains

Scripts to help work with AM processing chains

## am-chains-decode-procmcp.py

Show human readable messages for a specified processingMCP file
It uses the Django ORM to match the uuids in the file to the
corresponding entries in the related Dashboard models
(MicroServiceChainLink, etc)

Use the python interpreter of the MCP dashboard virtualenv:
$ /usr/share/python/archivematica-dashboard/bin/python am-chains-decode-procmcp.py <processingMCPfile.xml>

```
$ /usr/share/python/archivematica-dashboard/bin/python am-chains-decode-procmcp.py /var/archivematica/shared
Directory/sharedMicroServiceTasksConfigs/processingMCPConfigs/defaultProcessingMCP.xml
appliesTo: 56eebd45-5600-4768-a8c2-ec0114555a3d
goToChain: e9eaef1e-c2e0-4e3b-b942-bfb537162795
appliesTo (MicroServiceChainLink): Generate transfer structure report
goToChain (MicroServiceChain): No
----
appliesTo: 01c651cb-c174-4ba4-b985-1d87a44d6754
goToChain: 414da421-b83f-4648-895f-a34840e3c3f5
appliesTo (MicroServiceChainLink): Select compression level
goToChain (MicroServiceChain) not found, looking in MicroServiceChoiceReplacementtDic...
goToChain (MicroServiceChoiceReplacementtDic): 5 - normal compression mode
----
appliesTo: 7a024896-c4f7-4808-a240-44c87c762bc5
goToChain: 3c1faec7-7e1e-4cdd-b3bd-e2f05f4baa9b
appliesTo (MicroServiceChainLink): Select pre-normalize file format identification command
goToChain (MicroServiceChain) not found, looking in MicroServiceChoiceReplacementtDic...
goToChain (MicroServiceChoiceReplacementtDic): Use existing data
----
appliesTo: eeb23509-57e2-4529-8857-9d62525db048
goToChain: 5727faac-88af-40e8-8c10-268644b0142d
appliesTo (MicroServiceChainLink): Reminder: add metadata if desired
goToChain (MicroServiceChain): Continue
----
appliesTo: 7079be6d-3a25-41e6-a481-cee5f352fe6e
goToChain: 1170e555-cd4e-4b2f-a3d6-bfb09e8fcc53
appliesTo (MicroServiceChainLink): Transcribe SIP contents
goToChain (MicroServiceChain) not found, looking in MicroServiceChoiceReplacementtDic...
goToChain (MicroServiceChoiceReplacementtDic): No
----
...
```