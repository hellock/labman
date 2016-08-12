import random
import string


def rand_str(len, case='any'):
    if case == 'any':
        str_set = string.ascii_letters + string.digits
    elif case == 'lower':
        str_set = string.ascii_lowercase + string.digits
    elif case == 'upper':
        str_set = string.ascii_uppercase + string.digits
    else:
        raise ValueError('case must be "lower", "upper" or "any"')
    return ''.join(random.choice(str_set) for i in range(len))
