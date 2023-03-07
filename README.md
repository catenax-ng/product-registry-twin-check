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
* [x] Describe configuration of check tool
* [x] Add check for different cases BomAsBuilt (Batch, SerialPartTypization) & BomAsPlanned Twins
* [x] Add check against the testdatafile
* [x] Add compare to testfiles

</details>

* [ ] Maybe: Write tests for checks(dont know how yet)
* [ ] Maybe: Wrapping config in a class
* [ ] Maybe: refactor config file
* [ ] TODO: Identify duplicates
* [ ] TODO: Check if globalAssetId's are missing in registry with expected globalAssetIds

## Description

This repository holds a script to check Digital Twins within the Registry.

## Getting Started

```python
pip install pandas requests tdqm PyYAML
```

1. Add a valid *client_id* and *client_secret* to the configuration file.
2. Add a list of valid BPN's to the configuration file, if you want to check BPN specific Twins, or let it out to check the whole registry.
3. Add a list of semanticId's you want to be checked.
4. Change the variable SETTINGS_FILENAME to a settings filename of choice e.g. 'settings_beta.yaml'
5. Start the programm e.g. **python main.py**

## Configuration

This description is built with example values, to give guidance which kind of information is necessary

```yaml
version: 1
client_id: s34                         # keycloack client id 
client_secret: aöklsdjföalksdjfölkasdj # keycloack secret
keycloack_host: https://centralidp.int.demo.catena-x.net # keycloack host
keycloack_realm: /auth/realms/CX-Central/protocol/openid-connect/token # keycloack realm
registry_url: https://semantics.int.demo.catena-x.net # URL of registry service
force_reload: True                     # True force programm to reload twins from registry and not use cache
semanticIds:                           # list of semanticId's to be checked
- semanticId: urn:bamm:io.catenax.serial_part_typization:1.1.0#SerialPartTypization
  linkedSpecificAssetIds:
    - specificAssetId: manufacturerId
      checkLevel: mandatory 
    - specificAssetId: manufacturerPartId
      checkLevel: optional
check_output_filename: DTRCheck       # output filename, this will be appended with 
                                      # date time and environment information
bpn:                                  # optional: list of specific bpn values which are beeing tested.
                                      # If config is missing whole registry entries will be checked
  - company: A
    name: Tier A
    value: BPNL0000000XXXXX
proxies:                              # proxy settings for get requests
  http: 
  https: 
edc_catalog_check: True               # Should an EDC Catalog check of each participant in the Network be done
edc_consumer_control_plane:           # EDC consumer control plane url from which the catalog shall be retrieved
test_data_dir: testdata               # directory where to place all testdata files to check content against
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
| **unique globalAssetId** | Checks if the globalAssetId has been registered twice |
| **aasId!=globalAssetId** | Checks if globalAssetId and aasId are different values |
| **valid semanticIds** | Checks if the semanticIds match the list you see above |
| **valid semanticIds info** | List of semanticIds which do not comply to the list you see above |
| **manufacturerId in specificAssetIds**| checks if manufacturerId key exists in specificAssetId |
| **manufacturerId in specificAssetIds info**| output of manufacturerId |
| **bpn** | BPN |
| **bpn schema** | checks if bpn matches the bpn schema |
| **partInstanceId in specificAssetIds** | checks if partInstanceId key exists in specificAssetId |
| **partInstanceId in specificAssetIds info** | output of partInstanceId |
| **manufacturerPartId in specificAssetIds** | checks if manufacturerPartId key exists in specificAssetId |
| **manufacturerPartId in specificAssetIds info** | output of manufacturerPartId |
| **optional customerPartId in specificAssetIds** | optional topics can be skipped for now |
| **optional customerPartId in specificAssetIds info**| optional info to customerPartId|  
| **optional assetLifecyclePhase in specificAssetIds**| optinal checks if assetLifecyclePhase key exists in specificAssetId|
| **optional assetLifecyclePhase in specificAssetIds info**|optional info to specificAssetId|
| **optional batchId in specificAssetIds**| optional check for batchId |
| **optional batchId in specificAssetIds info**| optional info to batchId check |
| **optional van in specificAssetIds**|optinal checks if van key exists in specificAssetId|
| **optional van in specificAssetIds info**|optional info to van|
| **twin bpn matches to expected bpn**|checks if BPN matches to BPN Values of the test data files|
| **twin globalAssetId matches to expected globalAssetId**|checks if globalAssetId matches to the globalAssetId's of the test data files|
| **check** | Final Result is PASSED when no FAILED exists in one row |
