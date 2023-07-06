""" Hysun He (hysun.he@oracle.com) @ 2023/07/06 """

import os
import time
import logging

from pathlib import Path

import oss_utils

logger = logging.getLogger(__name__)

_NOCHANGE_TIMEOUT_SECONDS = 15
_SCAN_DIR = oss_utils.WORK_DIR


def check_run_auto_upload(bucket):
    """ docstring """
    for (root_dir, _, files) in os.walk(_SCAN_DIR):
        for file in files:
            file_path = os.path.join(root_dir, file)
            diff_seconds = int(time.time() - Path(file_path).stat().st_mtime)
            if diff_seconds >= _NOCHANGE_TIMEOUT_SECONDS:
                dest_path = Path(file_path).relative_to(_SCAN_DIR)
                logger.debug('Upload file %s...', file)
                oss_utils.sync_object_storage(bucket, file_path, dest_path)
                logger.debug('Upload file %s...done', file)
                oss_utils.delete_file(file_name=file_path)
                logger.debug('Local file %s...deleted', file)
                __uploaded = __uploaded + 1


def run(bucket):
    """ docstring """
    while True:
        check_run_auto_upload(bucket)
        time.sleep(2)
