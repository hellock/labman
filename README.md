# LabMan

## Overview

LabMan is a laboratory management system designed for [MMLab](http://mmlab.ie.cuhk.edu.hk/). This web-based system offers convenience for the following purposes:
- Member management
- Publication management
- Facility management

## Requirements
- Python 3.3+
- MongoDB

## Run
### Create a virtual enrironment (optional but recommended)
For OSX
``` shell
venv
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
- [ ] Register page
- [ ] Check name collision when adding a new user or registering
- [ ] Implement "remember me" checkbox
- [ ] Upload avatar
- [x] Change password
- [ ] Admin settings, such as set the auth level of members
- [x] Select supervisor instead of inputting
- [x] Show all members according to the admission year and position
- [ ] Make supervisor on the member overview page clickable
- [ ] Delete publications
- [ ] Notification module
- [ ] Log users' activities
- [ ] Facility management
- [ ] Show statistics
