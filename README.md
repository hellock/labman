# LabMan

## Overview
LabMan is a laboratory management system designed for [MMLab](http://mmlab.ie.cuhk.edu.hk/). This web-based system offers convenience for the following purposes:
- Member management
- Publication management
- Facility management

## Requirements
- Python 3.3+ (Python 2.7+ should be ok but not tested)
- MongoDB

## Run
### Create a virtual enrironment (optional but recommended)
``` shell
# For OSX with python3 installed through brew
venv ./venv
source venv/bin/activate
# For Ubuntu 16.04
# If an error is thrown out when creating a virtual environment, you can first create it without pip, then install pip manually.
sudo apt-get install python3-venv
python3 -m venv --without-pip ./venv
source venv/bin/activate
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
deactivate
source venv/bin/activate
```

### Install dependencies
- Python dependencies

    ``` shell
    pip3 install -r requirements.txt
    ```

- MongoDB

    ``` shell
    brew install mongodb # For OSX
    sudo apt-get install mongodb # For Ubuntu
    ```

### Start mongodb service
You can either use the default directory to store the database data or specify a directory to store it.
``` shell
mkdir dbdata
mongod --dbpath dbdata
```

### Init database
``` shell
./initdb.py
```
This script will create databases as well as an initial admin account with random password, the output should be like the following:
```
Initializing the database...
Initialization done
Initial admin username: admin, password: ln8nWjX8
```

### Run the app
``` shell
./run.py
```

## TODO list
- [x] Use configuration file
- [x] Register page
- [x] Check name collision when adding a new user or registering
- [ ] Implement "remember me" checkbox
- [x] Upload avatar
- [x] Change password
- [ ] Admin settings, such as set the auth level of members
- [x] Select supervisor instead of inputting
- [x] Show all members according to the admission year and position
- [ ] Make supervisor on the member overview page clickable
- [ ] Delete publications
- [x] Support submitting forms besides bibtex to add publications
- [ ] Notification module
- [ ] Log users' activities
- [x] Search box
- [ ] Facility management
- [x] Show statistics
- [x] Support candidates and alumni
- [x] Design an icon for LabMan
