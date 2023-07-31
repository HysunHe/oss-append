""" Hysun He (hysun.he@oracle.com) @ 2023/07/06 """

import os
import logging
from concurrent.futures import ThreadPoolExecutor
import oss_utils

logger = logging.getLogger(__name__)


def task(bucket_name, src_file, dest_file):
    """ docstring """
    try:
        oss_utils.sync_object_storage(bucket_name, src_file, dest_file)
    except Exception as err:  # pylint: disable=broad-except
        logger.error('Unexpected error: %s', str(err))


def run():
    """ docstring """
    cpu_count = os.cpu_count()
    parallel = cpu_count - 2 if cpu_count and cpu_count > 2 else 1

    with ThreadPoolExecutor(max_workers=parallel) as executor:
        while True:
            (bucket_name, src_file,
             dest_file) = oss_utils.SYNC_TASK_QUEUE.get(block=True)
            executor.submit(task, bucket_name, src_file, dest_file)
