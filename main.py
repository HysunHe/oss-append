""" Hysun He (hysun.he@oracle.com) @ 2023/07/06 """

from threading import Thread

import auto_upload
import oss_append

if __name__ == '__main__':
    thread = Thread(target=auto_upload.run, args=('test', ), daemon=True)
    thread.start()

    oss_append.run()
