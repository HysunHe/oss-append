""" Hysun He (hysun.he@oracle.com) @ 2023/08/01 """

import os
import logging
from concurrent.futures import ThreadPoolExecutor
import my_utils
from task_queue import TqMgr

logger = logging.getLogger(__name__)


def task(bucket_name, src_file, dest_file):
    """ docstring """
    try:
        my_utils.sync_object_storage(bucket_name, src_file, dest_file)
    except Exception as err:  # pylint: disable=broad-except
        logger.error('Unexpected error: %s', str(err))


def run():
    """ docstring """
    cpu_count = os.cpu_count()
    parallel = cpu_count - 2 if cpu_count and cpu_count > 2 else 1

    with ThreadPoolExecutor(max_workers=parallel) as executor:
        while True:
            (bucket_name, src_file, dest_file) = TqMgr.inst().poll()
            executor.submit(task, bucket_name, src_file, dest_file)
