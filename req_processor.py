""" Hysun He (hysun.he@oracle.com) @ 2023/07/04 """

import os
import logging
import base64

from flask import Flask, request
from gevent import pywsgi

import oss_utils
from devlog import my_logger as log_utils
from oci_config import OciConf as oci_conf

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/test-upload', methods=['POST'])
@log_utils.debug_enabled(logger)
def test_upload():
    """ docstring """
    video_bytes = request.data
    with open('/tmp/dummyvideo.mp4', 'wb') as file:
        file.write(video_bytes)
    return 'Good'


@app.route('/write-json', methods=['POST'])
@log_utils.debug_enabled(logger)
def write_json():
    """ JSON payload """
    auth_result = authorize_request(request)
    if auth_result is not None:
        return auth_result

    data = request.get_json(force=True)
    bucket = data['bucket']
    file_name = data['name']
    destination = file_name
    file_position = int('0' if 'position' not in data else data['position'])
    whence = 2 if 'position' not in data or file_position < 0 else 0
    content_base64 = data['content']
    append = data['append']
    content_bytes = base64.b64decode(content_base64)
    logger.debug('file_name: %s', file_name)
    logger.debug('file_position: %d, %d', file_position, whence)
    logger.debug('append: %s', append)

    pos = handle_content(file_name=file_name,
                         file_position=file_position,
                         whence=whence,
                         content_bytes=content_bytes,
                         append=append,
                         bucket=bucket,
                         destination=destination)

    # pylint: disable=line-too-long
    location = f'https://objectstorage.{oci_conf.get_region()}.oraclecloud.com/n/{oci_conf.get_namespace()}/b/{bucket}/o/{file_name}' if append and str(
        append).lower() not in ('true', '1') else ''
    return {'status': 'ok', 'current_file_position': pos, 'location': location}


@app.route('/write-bytes', methods=['POST'])
@log_utils.debug_enabled(logger)
def write_bytes():
    """ Bytes payload """
    auth_result = authorize_request(request)
    if auth_result is not None:
        return auth_result

    content_bytes = request.get_data()
    bucket = request.args.get('bucket')
    file_name = request.args.get('name')
    append = request.args.get('append')
    file_position = int('0' if not request.args.get('position') else request.
                        args.get('position'))
    destination = file_name
    whence = 2 if not request.args.get('position') or file_position < 0 else 0
    logger.debug('file_name: %s', file_name)
    logger.debug('file_position: %d, %d', file_position, whence)
    logger.debug('append: %s', append)

    pos = handle_content(file_name=file_name,
                         file_position=file_position,
                         whence=whence,
                         content_bytes=content_bytes,
                         append=append,
                         bucket=bucket,
                         destination=destination)

    # pylint: disable=line-too-long
    location = f'https://objectstorage.{oci_conf.get_region()}.oraclecloud.com/n/{oci_conf.get_namespace()}/b/{bucket}/o/{file_name}' if append and str(
        append).lower() not in ('true', '1') else ''
    return {'status': 'ok', 'current_file_position': pos, 'location': location}


def authorize_request(req):
    """ docstring """
    headers = req.headers
    x_amz_date = headers.get('X-Amz-Date')
    assert x_amz_date is not None, 'Mising required header: X-Amz-Date'
    authorization = headers.get('Authorization')
    assert authorization is not None, 'Mising required header: Authorization'
    auth_local = oss_utils.gen_auth_md5(x_amz_date)
    if authorization != auth_local:
        return 'Unauthorized', 401
    return None


# @log_utils.debug_enabled(logger)
# pylint: disable=too-many-arguments
def handle_content(file_name, file_position, whence, content_bytes, append,
                   bucket, destination) -> int:
    """ docstring """
    file_fullname = f'{oss_utils.WORK_DIR}/{file_name}'
    oss_utils.ensure_file_exists(file_fullname)

    with open(file_fullname, 'rb+') as dest_file:
        logger.debug('Write content to file. file_position: %d, %d',
                     file_position, whence)
        dest_file.seek(0 if file_position < 0 else file_position, whence)
        dest_file.write(content_bytes)
        current_position = dest_file.tell()

    if append and str(append).lower() not in ('true', '1'):
        oss_utils.enqueue_task(bucket, file_fullname, destination)

    return current_position


@log_utils.debug_enabled(logger)
def run():
    """ docstring """
    # app.run(host='0.0.0.0') # Dev mode
    host = os.environ.get('SERVER_HOST', '0.0.0.0')
    port = os.environ.get('SERVER_LISTEN_PORT', 5000)
    server = pywsgi.WSGIServer((host, port), app)
    server.serve_forever()
