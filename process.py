#!/usr/bin/python3
import sys
from pprint import pprint

time_begin = 0
time_interval = 50
file_path = ''


def discard(file):
    """
    读取前面无用的行
    :param file:
    :return:
    """
    while True:
        previous = file.tell()
        line = file.readline()
        if line.startswith('$scope'):
            file.seek(previous)
            return


def discard_time(file, end_time):
    """
    抛弃开始时间前面的额行
    :param file:
    :param end_time:
    :return:
    """
    while True:
        previous = file.tell()
        line = file.readline()
        if line.startswith('#'):
            time = int(line[1:])
            if time > end_time:
                file.seek(previous)
                return True


def create_module(file, a_line):
    """
    读取module
    :param file:
    :param a_line:
    :return: module 的 dictionary
    """
    data = {}
    keys = {}
    module_name = a_line.split()[2]
    while True:
        line = file.readline()
        if line.startswith('$upscope') or not line:
            return module_name, data, keys
        a_list = line.split()
        if not a_list:
            return module_name, data, keys
        # print(a_list)
        keys[a_list[3]] = {'value': 0, '1st': module_name, '2nd': a_list[4]}
        # if module_name == 'U16':
        #     print(module_name, a_list', =========================')
        data[a_list[4]] = {'name': a_list[3], 'value': 0}


def scope(file):
    """
    读取scope
    :param file:
    :return: 按不同方式组织起来的 结构。
    """
    data = {}
    keys = {}
    while True:
        line = file.readline()
        if line.startswith('$scope'):
            module_name, module_body, module_keys = create_module(file, line)
            # pprint(module_name)
            # pprint(module_body)
            # pprint(module_keys)
            if module_name in data:
                data[module_name].update(module_body)
            else:
                data[module_name] = module_body
            keys.update(module_keys)
        if line.startswith('$enddefinitions'):
            # if line.startswith('$dumpvars'):
            return data, keys


def read_var(file, keys):
    """
    读取vars
    :param file:
    :param keys:
    :return:
    """
    discard_time(file, time_begin)
    hits = 0
    end_time = time_interval
    while True:
        time_keys, time_hits, will_continue = time_var(file, keys, end_time)
        if time_hits > hits:
            for a_key in keys.keys():
                keys[a_key]['value'] = time_keys[a_key]
            print('time', end_time - time_interval, '-', end_time, 'has total hits', time_hits, ', larger than', hits)
            hits = time_hits
        if not will_continue:
            return keys
        end_time += time_interval


def time_var(file, all_key, end_time):
    """
    读取每个时间段并返回 dictionary
    :param file:
    :param all_key: all the key
    :param end_time: the time to end this count
    :return: {key: value}, total_hit, if_continue?
    """
    keys = dict.fromkeys(all_key, 0)
    total_hit = 0
    while True:
        line = file.readline()
        previous = file.tell()
        if not line:
            return keys, total_hit, False
        if line.startswith('$end') or line.startswith('$dumpvars'):
            continue
        if line.startswith('#'):
            time = int(line[1:])
            if time > end_time:
                file.seek(previous)
                return keys, total_hit, True
            else:
                continue
        temp = line.split()
        if not temp:
            continue
        if len(temp) > 1:
            line = temp[1]
        label = line[1:].rstrip()
        keys[label] += 1
        total_hit += 1
        # print(label, keys[label])


if __name__ == '__main__':
    if len(sys.argv) == 4:
        time_begin = int(sys.argv[1])
        time_interval = int(sys.argv[2])
        file_path = sys.argv[3]
    else:
        file_path = sys.argv[1]
    with open(file_path) as f:
        discard(f)
        my_module, my_keys = scope(f)
        # print('====================================================')
        # pprint(my_module)
        # pprint(my_keys)
        my_keys = read_var(f, my_keys)
        print('=====================got all the keys and count===============================')
        # pprint(my_keys)
        # print(my_keys.keys())
        for each_key in my_keys.values():
            # pprint(each_key)
            # print(each_key['1st'], my_module[each_key['1st']])
            my_module[each_key['1st']][each_key['2nd']]['value'] = each_key['value']
        # pprint(my_module)
    with open('keys.txt', 'w') as f:
        pprint(my_keys, f)
    with open('module.txt', 'w') as f:
        pprint(my_module, f)
