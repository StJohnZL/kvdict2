#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 
#  对kvdict进行性能测试
#  

import os
import sys
import time
import random
import kvdict2

def random_string(n):
    ret = ('%1d' % random.randint(0, 10)) * n
    return ret

def test_file(d):
    d.load(file_name)
    tm_begin = time.time()
    for k in key_list:
        s = d.find(k)
    during = time.time() - tm_begin
    sys.stderr.write("SEARCHING_KEYS : %d\n" % len(key_list))
    sys.stderr.write("USING_TIME     : %.3f(s)\n" % during)
    sys.stderr.write("AVERAGE_TIME   : %.3f(s)\n" % (during / len(key_list)))
    sys.stderr.write("QPS            : %.1f qps\n" % (len(key_list) / during))

if __name__=='__main__':
    test_num = 1000000
    key_length = 8
    value_length = 128

    sys.stderr.write("preparing data..\n")
    file_name = 'benchmark_data.txt'
    os.system('rm -rf %s' % file_name)

    key_list = []
    with open(file_name, 'w') as f:
        for i in range(test_num):
            key = random_string(key_length)
            value = random_string(value_length)
            f.write('%s\t%s\n' % (key, value))
            key_list.append(key)
            if i % 100000 == 0:
                sys.stderr.write("write %d record(s)\n" % i)
    sys.stderr.write("complete preparing.\n")

    key_list = sorted(key_list)
    
    d = kvdict2.FileIndexKVDict()
    sys.stderr.write("KEY_LENGTH    : %d\n" % key_length)
    sys.stderr.write("VALUE_LENGTH  : %d\n" % value_length)
    sys.stderr.write("TEST #1 LOAD IN DISK:\n")
    test_file(d)
    sys.stderr.write("TEST #2 LOAD IN MEMORY:\n")
    d = kvdict2.KVDict()
    test_file(d)

    os.system('rm -rf benchmark_data.txt')
