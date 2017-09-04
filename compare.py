#!/usr/bin/python3
import sys
from pprint import pprint
from ast import literal_eval

"""
compare two different routine.
"""
if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        data_1 = literal_eval(f.read())
    with open(sys.argv[2]) as f:
        data_2 = literal_eval(f.read())
    data_diff = {}
    first_level_keys = set(list(data_1.keys()) + list(data_2.keys()))
    print('number of 1st level keys:', len(first_level_keys))
    number_of_second_level_keys = 0
    for a_key in first_level_keys:
        routine_1 = data_1.setdefault(a_key, {})
        routine_2 = data_2.setdefault(a_key, {})
        data_diff[a_key] = {}
        second_level_keys = set(list(routine_1.keys()) + list(routine_2.keys()))
        number_of_second_level_keys += len(second_level_keys)
        for another_key in second_level_keys:
            if another_key not in routine_1:
                routine_1.setdefault(another_key, {'name': routine_2[another_key]['name'], 'value': 0})
            if another_key not in routine_2:
                routine_2.setdefault(another_key, {'name': routine_1[another_key]['name'], 'value': 0})
            data_diff[a_key][another_key] = {'name': routine_2[another_key]['name'],
                                             'value': routine_1[another_key]['value'] - routine_2[another_key]['value']}
    print('number of 2nd level keys:', len(first_level_keys))
    with open('diff.txt', 'w') as f:
        pprint(data_diff, f)

