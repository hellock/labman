# Global configuration variable
CONFIG = {
    'lab_name': 'Multimedia Laboratory',
    # database info
    'db': {
        'ip': 'localhost',
        'port': 27017,
        'name': 'mmlab'
    },
    # log configuration
    'log': {
        'level': 'INFO',
        # whether to use capped collections to support high-throughput operations
        'capped': False
    },
    # `mode` can be either 'debug' or 'deploy'
    'run_mode': 'debug',
    # list of positions to be chosen from
    'positions': ['Professor', 'PostDoc', 'PhD', 'MPhil', 'Master',
                  'RA', 'Intern', 'Others'],
    # predefined conference names that will be shown as select options
    'conferences': [
        'The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)',
        'The IEEE International Conference on Computer Vision (ICCV)',
        'European Conference on Computer Vision (ECCV)',
        'Conference on Neural Information Processing Systems (NIPS)'
        'The International Conference on Machine Learning (ICML)',
        'AAAI Conference on Artificial Intelligence'
    ],
    # predefined journal names that will be shown as select options
    'journals': [
        'IEEE Transactions on Pattern Analysis and Machine Intelligence (PAMI)',
        'International Journal of Computer Vision (IJCV)'
    ]
}
