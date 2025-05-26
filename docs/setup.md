# WaypointAI Quickstart
This document lays out how to set up and run the WaypointAI app as well as things to know.

The app has one git repos named as **wc_ai**.

## Requirements

- Python
- MongoDB

## Getting started

These are the basic steps you need to follow to get the app up and running.

1. Clone the repo.
2. Inside the repo directory create a virtual enivornment by using this command `python3 -m venv my-virtual-environment` (you can name it anything **my-virutal-enviroment**)
3. Activate the venv using this command `source venv/bin/activate` (**venv** is the name you have given to your venv, according to above command it would be like `source my-virtual-environment/bin/activate`)
4. For deactivating the venv use command `deactivate`
5. Now install the required packages by command `pip install -r /path/to/requirements.txt`
6. After installing the packages, run command `playwright install`


