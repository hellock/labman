# LabMan

## Overview
LabMan is a laboratory management system originally designed for [MMLab](http://mmlab.ie.cuhk.edu.hk/). This web-based system provides convenience for:
- Member management
- Publication management
- Facility management (not completed)
- Information statistics

## Requirements
- Python 3.3+ (Python 2.7+ should be ok but not tested)
- MongoDB (version 3.2+ recommended)

## Run
### Create a virtual enrironment (optional but recommended)
``` shell
# For OSX with python3 installed through brew
venv ./venv
source venv/bin/activate
# For Linux
python3 -m venv ./venv
```
There may be errors thrown out when creating virtual environment on some distributions of Linux, you can first create it without pip, then install pip manually, taking Ubuntu 16.04 LTS for example.
``` shell
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

### Modify the configuration file
The configuration file `app/config.py` is like the following.
``` python
# Global configuration variable
CONFIG = {
    # lab name will be shown on the signin page
    'lab_name': 'Multimedia Laboratory',
    # database info
    'db': {
        'ip': 'localhost',
        'port': 27017,
        'name': 'mmlab'
    },
    # log configuration
    'log': {
        # logging levels: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        'level': 'INFO',
        # whether to use capped collections to support high-throughput operations
        'capped': False
    },
    # `mode` can be either 'debug' or 'deploy'
    'run_mode': 'debug',
    # positions to be chosen from, list of tuples
    'positions': [
        ('1', 'Professor'),
        ('2', 'Postdoctoral Researcher'),
        ('3', 'PhD'),
        ('4', 'MPhil'),
        ('5', 'Master'),
        ('6', 'Research Assistant'),
        ('7', 'Intern'),
        ('0', 'Others'),
    ],
    # indicate which positions belong to supervisors
    'supervisor_positions': ['1'],
    # predefined conference names that will be shown as select options
    'conferences': [
        'The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)',
        'The IEEE International Conference on Computer Vision (ICCV)',
        'European Conference on Computer Vision (ECCV)',
        'Conference on Neural Information Processing Systems (NIPS)',
        'The International Conference on Machine Learning (ICML)',
        'AAAI Conference on Artificial Intelligence'
    ],
    # predefined journal names that will be shown as select options
    'journals': [
        'IEEE Transactions on Pattern Analysis and Machine Intelligence (PAMI)',
        'International Journal of Computer Vision (IJCV)'
    ]
}
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
- [x] Admin settings, such as set the auth level of members
- [x] Select supervisor instead of inputting
- [x] Show all members according to the admission year and position
- [x] Make supervisor on the member overview page clickable
- [ ] Delete publications
- [x] Support submitting forms besides bibtex to add publications
- [ ] Notification module
- [x] Log users' activities
- [x] Search box
- [ ] Facility management
- [x] Show statistics
- [x] Support candidates and alumni
- [x] Design an icon for LabMan
