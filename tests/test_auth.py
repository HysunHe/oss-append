import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import oss_utils

encoded_str = oss_utils.gen_auth_md5('20230724T023712Z')
print(encoded_str)