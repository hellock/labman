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
