# product-registry-twin-check

This repository holds a script to check Digital Twins within the Registry.

Currently the script checks the following:

* check1 - checks if the global AssetId is different to the aasID
* check2 - checks if the semanticIDs are of a valid structure
* check3 - checks if a manaufacturerId is specified in the specificAssetIds
* check4 - checks if an ID has a valid URN:UUID Format

## Getting Started

Add a valid client_id and client_secret to the configuration file and remove the "copy" from the filename so that its name is **settings.yaml**.
Select or add a BPN to the list of BPN's and start the programm with **python main.py**
