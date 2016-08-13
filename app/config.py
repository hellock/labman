# Global configuration variable
CONFIG = {
    'lab_name': 'Multimedia Laboratory',
    # database info
    'db': {
        'ip': 'localhost',
        'port': 27017,
        'name': 'mmlab'
    },
    # `mode` can be either 'debug' or 'deploy'
    'run_mode': 'debug',
    # list of positions to be chosen from
    'positions': ['Professor', 'PostDoc', 'PhD', 'MPhil', 'Master',
                  'RA', 'Intern', 'Others']
}
