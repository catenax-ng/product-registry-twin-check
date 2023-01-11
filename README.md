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

</details>

* [ ] Maybe: Write tests for checks(dont know how yet)
* [ ] Maybe: Wrapping config in a class
* [ ] Maybe: refactor config file
* [ ] TODO: Add check against the testdatafile
* [ ] TODO: Add check for different cases BomAsBuilt & BomAsPlanned Twins
* [ ] TODO: Get specification from Markus Keidl to specific Values and globalAssetIds
* [ ] TODO: Describe configuration of check tool

## Description

This repository holds a script to check Digital Twins within the Registry.

## Getting Started

1. Add a valid *client_id* and *client_secret* to the configuration file.
2. Add a list of valid BPN's to the configuration file, if you want to check BPN specific Twins, or let it out to check the whole registry.
3. Add a list of semanticId's you want to be checked.
4. Change the variable SETTINGS_FILENAME to a settings filename of choice e.g. 'settings_beta.yaml'
5. Start the programm e.g. **python main.py**

## Debugging

If you need further information while running this programm set the option **Level** to **DEBUG** on the root level in the **logging.yaml** file.

## Extracting SemanticId's from Testdata file

On a linux based machine you can extract a list of semanticId's from the testdata file with the following snippet.

```bash
cat CX_Testdata_v1.4.1-AsPlanned.json | jq '."https://catenax.io/schema/TestDataContainer/1.0.0" | .[] | keys' | sort | uniq | grep urn
```
