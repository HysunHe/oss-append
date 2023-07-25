import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import oss_utils

encoded_str = oss_utils.gen_auth_md5('20230724T023712Z')
print(encoded_str)

dir1 = os.path.dirname('aaa/bbb/ddd/abc.txt')
base1 = os.path.basename('aaa/bbb/ddd/abc.txt')
print(f'dir1={dir1}, base1={base1}')

dir2 = os.path.dirname('abc.txt')
base2 = os.path.basename('abc.txt')
print(f'dir2={dir2}, base2={base2}')

dir3 = os.path.dirname(os.path.normpath('///aaa/bbb//ddd/abc.txt'))
dir4 = os.path.join('aaa', os.pardir)
print(f'dir3={dir3}, dir4={dir4}')

print(f'{os.path.isfile("/tmp/file_fullname.txt")}')
print(f'{os.path.abspath("/tmp/file_fullname.txt")}')
print(f'{os.path.abspath("file_fullname.txt")}')