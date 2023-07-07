""" Hysun He (hysun.he@oracle.com) @ 2023/07/06 """
import os
from threading import Thread

import auto_upload
import oss_append


def run():
    """ docstring """
    bucket = os.environ.get('OSS_BUCKET')
    timeout = os.environ.get('NO_UPDATE_TIMEOUT_SECONDS')
    if not bucket:
        raise ValueError('Missing required env variable [OSS_BUCKET]')

    thread = Thread(target=auto_upload.run,
                    args=(
                        bucket,
                        timeout,
                    ),
                    daemon=True)
    thread.start()

    oss_append.run()


if __name__ == '__main__':
    run()
