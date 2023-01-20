# product-registry-twin-check

## Todos

<details>
  <summary>Done Tasks</summary>

* [x] CRITICAL SOLVE GLOBALS ISSUE ==> initialize only once if inctance exists?
* [x] ✅ Add functionality to force reload
* [x] ✅ Refactor code into Classes and restructure programm
* [x] ✅ Add functionality fo Multiple BPN's
* [x] ✅ draw Statusbar
* [x] ✅ Proxy settings variable
* [x] ✅ Documentation
* [x] ✅ Refactor getTwinsByBPN force reload strategy (a pickl per bpn => abstraction a lot easier)
* [x] add list of valid semanticIds into the configuration
* [x] Refactor Checks and Checkclass
* [x] manufactureId Logic is not tested correctly
* [x] Add more information to resultset to identify an object
* [x] Maybe: validate EDC Endpoints found. Make it nice Code
* [x] TODO: Describe configuration of check tool

</details>

* [ ] Maybe: Write tests for checks(dont know how yet)
* [ ] Maybe: Wrapping config in a class
* [ ] Maybe: refactor config file
* [ ] TODO: Add check against the testdatafile
* [ ] TODO: Add check for different cases BomAsBuilt & BomAsPlanned Twins

## Description

This repository holds a script to check Digital Twins within the Registry.

## Getting Started

1. Add a valid *client_id* and *client_secret* to the configuration file.
2. Add a list of valid BPN's to the configuration file, if you want to check BPN specific Twins, or let it out to check the whole registry.
3. Add a list of semanticId's you want to be checked.
4. Change the variable SETTINGS_FILENAME to a settings filename of choice e.g. 'settings_beta.yaml'
5. Start the programm e.g. **python main.py**

## Configuration

```yaml
version: 1
client_id: ''                     # keycloack client id 
client_secret: ''                 # keycloack secret
keycloack_host: ''                # keycloack host
keycloack_realm: ''               # keycloack realm path
registry_url: ''                  # URL of registry service
force_reload: True                # True force programm to reload twins from 
                                  # registry and not use cache

semanticIds:                      # list of semanticId's to be checked
  - 'urn:bamm:io.catenax.serial_part_typization:1.1.0#SerialPartTypization'
  - 'urn:bamm:io.catenax.assembly_part_relationship:1.1.#AssemblyPartRelationship'

check_output_filename: 'DTRCheck' # output filename, this will be appended
                                  # with date time and environment information

bpn:                              # OPTIONAL: list of specific bpn values which 
                                  # are beeing tested. If config is missing all 
                                  # registry entries will be checked
  - {'company':'A', 'name': 'Tier A','value':'BPNL0000000XXXXX'}
  - {'company':'B', 'name': 'Sub Tier A','value':'BPNL0000000YYYYY'}

proxies: { 'http':'', 'https':''} # proxy settings for get requests

edc_catalog_check: True           # Should an EDC Catalog check of each participant
                                  # in the Network be done.

edc_consumer_control_plane: ''    # EDC consumer control plane url from which the 
                                  # catalog shall be retrieved.
edc_catalog_check: True # Should an EDC Catalog check of each participant in the Network be done
edc_consumer_control_plane: '' # EDC consumer control plane url from which the catalog shall be retrieved
```

## Debugging

If you need further information while running this programm set the option **Level** to **DEBUG** on the root level in the **logging.yaml** file.

## Extracting SemanticId's from Testdata file

On a linux based machine you can extract a list of semanticId's from the testdata file with the following snippet.

```bash
cat CX_Testdata_v1.4.1-AsPlanned.json | \
 jq '."https://catenax.io/schema/TestDataContainer/1.0.0" | .[] | keys' | \
 sort | uniq | grep urn
```

## Output File explained

| column name | column description |
|----|----|
| **aasid** | aasId of twin to identify object |
| **status** | Python program check (only for internal purposes) |
| **aas uuid:urn format**| Checks if aasId complies to the uuid:urn format |
| **globalAssetId exists** | Checks if the key globalAssetId exists |
| **globalAssetId uuid:urn format** | Checks if globalAssetId complies to the uuid:urn format |
| **aasId!=globalAssetId** | Checks if globalAssetId and aasId are different values |
| **valid semanticIds** | Checks if the semanticIds match the list you see above |
| **valid semanticIds info** | List of semanticIds which do not comply to the list you see above |
| **manufacturerId in specificAssetIds**| checks if manufacturerId key exists in specificAssetId |
| **manufacturerId in specificAssetIds info**| output of manufacturerId |
| **bpn** | BPN |
| **bpn schema** | checks if bpn matches the bpn schema |
| **optional partInstanceId in specificAssetIds** | checks if partInstanceId key exists in specificAssetId |
| **optioinal partInstanceId in specificAssetIds info** | output of partInstanceId |
| **manufacturerPartId in specificAssetIds** | checks if manufacturerPartId key exists in specificAssetId |
| **manufacturerPartId in specificAssetIds info** | output of manufacturerPartId |
| **optional customerPartId in specificAssetIds** | optional topics can be skipped for now |
| **optional customerPartId in specificAssetIds info**| optional info to customerPartId|  
| **optional batchId in specificAssetIds**| optional check for batchId |
| **optional batchId in specificAssetIds info**| optional info to batchId check |
| **check** | Final Result is PASSED when no FAILED exists in one row |
