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

## Description

This repository holds a script to check Digital Twins within the Registry.

Currently the script checks the following:

* check1 - checks if the global AssetId is different to the aasID
* check2 - checks if the semanticIDs are of a valid structure
* check3 - checks if a manaufacturerId is specified in the specificAssetIds
* check4 - checks if an ID has a valid URN:UUID Format

## Getting Started

Add a valid *client_id* and *client_secret* to the configuration file and remove the "copy" from the filename so that its name is **settings.yaml**.
Select or add a BPN to the list of BPN's and start the programm with **python main.py**

## Debugging

If you need further information while running this programm set the option **Level** to **DEBUG** on the root level in the **logging.yaml** file.

