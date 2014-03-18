from itertools import groupby

from path_helpers import path


def traverse(data):
    '''
    Recursively traverse entries to return Arduino-config values in a
    nested-dictionary.
    '''
    results = {}
    if data[0][0]:
        for key, group in groupby([d for d in data if d[0]], lambda x: x[0][0]):
            group_data = list(group)
            results[key] = traverse([(item[0][1:], item[1])
                                     for item in group_data])
        return results
    else:
        return data[0][1]


def parse_config(config_path):
    '''
    Return a nested dictionary containing configuration from an
    Arduino-formatted configuration file _(e.g., `platform.txt`,
    `boards.txt`)_.
    '''
    config_data = sorted([line.strip() for line in path(config_path).lines()
                          if line.strip() and not line.startswith('#')])
    config_cleaned_data = []
    for d in config_data:
        if '=' in d:
            split_position = d.index('=')
            key = d[:split_position].split('.')
            value = d[split_position + 1:]
            config_cleaned_data.append([key, value])
    return traverse(config_cleaned_data)


def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                #raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
                print ('[warning] Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
