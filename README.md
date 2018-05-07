# cloudDrive

Tool to aggregate storage across multiple cloud providers. Multithreaded and chunk use for speed.

Using Box, Google Drive, and Dropbox python modules.

Right now, takes in a .txt file splits it into chunks on "Splitting Text" and uploads it to 3 cloud providers.

Also able to list and download/reassemble.

Uses a 'ledger' to track file and locations. Without this files will be lost

requirements
-python2.7
-boxsdk
-pydrive
-dropbox

Several client secrets and env_vars must be configured for each module.

For Box:
In a file "box.cfg", place CLIENT_ID, CLIENT_SECRET, and ACCESS_TOKEN on seperate lines.

For Dropbox:
Add an enviroment variable "DBTOKEN" with your acess token.

For Drive:
See https://pythonhosted.org/PyDrive/oauth.html

@todo 
integate redundanacy for files a "backup" 
bash pipeline
