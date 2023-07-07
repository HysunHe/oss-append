""" Hysun He (hysun.he@oracle.com) @ 2023/07/04 """

import logging
import base64
import time
import os

from flask import Flask, request
from gevent import pywsgi
from moviepy.editor import VideoFileClip, concatenate

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
    """ Sample call to the API:
        binary_data = bytes('data to be encoded: 你好', 'utf-8')
        requests.post(
            url='http://localhost:5000/write-json',
            headers={'Content-Type': 'application/json'},
            json={
                "bucket": "Hysun_DianJiang",
                "name":"demo2.bin",
                "position": 260,
                "content": base64.b64encode(binary_data).decode(encoding='utf-8'),
                "append": "1"
            }
        )
    """
    data = request.get_json(force=True)
    bucket = data['bucket']
    file_name = data['name']
    # destination = file_name if 'destination' not in data or not data[
    #     'destination'] else data['destination']
    destination = file_name
    file_position = int('0' if 'position' not in data else data['position'])
    whence = 2 if 'position' not in data or file_position < 0 else 0
    content_base64 = data['content']
    append = data['append']
    content_bytes = base64.b64decode(content_base64)
    logger.debug('file_name: %s', file_name)
    logger.debug('file_position: %d, %d', file_position, whence)
    logger.debug('append: %s', append)

    oss_utils.ensure_file_exists(file_name=file_name)

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
    # pylint: disable=line-too-long
    """ Sample call to this API:
        binary_data = bytes('data to be encoded: 你好', 'utf-8')
        url = 'http://localhost:5000/write-bytes?bucket=Hysun_DianJiang&name=demo3.bin&position=0&append=1'
        response = requests.post(url=url, data=binary_data)
    """
    content_bytes = request.get_data()
    bucket = request.args.get('bucket')
    file_name = request.args.get('name')
    append = request.args.get('append')
    file_position = int('0' if not request.args.get('position') else request.
                        args.get('position'))
    # destination = file_name if not request.args.get(
    #     'destination') else request.args.get('destination')
    destination = file_name
    whence = 2 if not request.args.get('position') or file_position < 0 else 0
    logger.debug('file_name: %s', file_name)
    logger.debug('file_position: %d, %d', file_position, whence)
    logger.debug('append: %s', append)

    oss_utils.ensure_file_exists(file_name=file_name)

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


@app.route('/append-mp4-json', methods=['POST'])
@log_utils.debug_enabled(logger)
def write_mp4_json():
    # pylint: disable=line-too-long
    """ Sample call to this API:
        url = 'http://localhost:5000/append-mp4-json'
    """
    data = request.get_json(force=True)
    bucket = data['bucket']
    file_name = data['name']
    destination = file_name
    content_base64 = data['content']
    append = data['append']
    content_bytes = base64.b64decode(content_base64)
    logger.debug('file_name: %s', file_name)
    logger.debug('append: %s', append)

    handle_content_video(file_name=file_name,
                         content_bytes=content_bytes,
                         append=append,
                         bucket=bucket,
                         destination=destination)

    # pylint: disable=line-too-long
    location = f'https://objectstorage.{oci_conf.get_region()}.oraclecloud.com/n/{oci_conf.get_namespace()}/b/{bucket}/o/{file_name}' if append and str(
        append).lower() not in ('true', '1') else ''
    return {'status': 'ok', 'current_file_position': -1, 'location': location}


@app.route('/append-mp4', methods=['POST'])
@log_utils.debug_enabled(logger)
def write_mp4():
    # pylint: disable=line-too-long
    """ Sample call to this API:
        url = 'http://localhost:5000/append-mp4?bucket=Hysun_DianJiang&name=demo3.bin&append=1'
        response = requests.post(url=url, data=video_bytes)
    """
    content_bytes = request.get_data()
    bucket = request.args.get('bucket')
    file_name = request.args.get('name')
    append = request.args.get('append')
    # destination = file_name if not request.args.get(
    #     'destination') else request.args.get('destination')
    destination = file_name
    logger.debug('file_name: %s', file_name)
    logger.debug('append: %s', append)
    handle_content_video(file_name=file_name,
                         content_bytes=content_bytes,
                         append=append,
                         bucket=bucket,
                         destination=destination)


    # pylint: disable=line-too-long
    location = f'https://objectstorage.{oci_conf.get_region()}.oraclecloud.com/n/{oci_conf.get_namespace()}/b/{bucket}/o/{file_name}' if append and str(
        append).lower() not in ('true', '1') else ''
    return {'status': 'ok', 'current_file_position': -1, 'location': location}


def handle_content_video(file_name, content_bytes, append, bucket,
                         destination):
    """ docstring """
    file_fullname = f'{oss_utils.WORK_DIR}/{file_name}'
    oss_utils.ensure_dir_exists(file_fullname)

    tmp_clip_file = f'/tmp/{file_name}_{int(time.time())}.mp4'
    with open(tmp_clip_file, 'wb') as clip_file:
        clip_file.write(content_bytes)
    this_clip = VideoFileClip(tmp_clip_file)

    if os.path.exists(file_fullname):
        try:
            exist_clips = VideoFileClip(file_fullname)
            new_clips = concatenate([exist_clips, this_clip])
        except IOError as err:
            logger.warning(str(err))
            new_clips = this_clip
    else:
        new_clips = this_clip

    oss_utils.delete_file(file_fullname)
    new_clips.write_videofile(file_fullname)
    

    if append and str(append).lower() not in ('true', '1'):
        logger.debug('Upload file %s...', file_name)
        oss_utils.sync_object_storage(bucket, file_fullname, destination)
        logger.debug('Upload file %s...done', file_name)
        oss_utils.delete_file(file_name=file_fullname)
        logger.debug('Local file %s...deleted', file_name)


# @log_utils.debug_enabled(logger)
# pylint: disable=too-many-arguments
def handle_content(file_name, file_position, whence, content_bytes, append,
                   bucket, destination) -> int:
    """ docstring """
    file_fullname = f'{oss_utils.WORK_DIR}/{file_name}'
    with open(file_fullname, 'rb+') as dest_file:
        logger.debug('Write content to file. file_position: %d, %d',
                     file_position, whence)
        dest_file.seek(0 if file_position < 0 else file_position, whence)
        dest_file.write(content_bytes)
        current_position = dest_file.tell()

    if append and str(append).lower() not in ('true', '1'):
        logger.debug('Upload file %s...', file_name)
        oss_utils.sync_object_storage(bucket, file_fullname, destination)
        logger.debug('Upload file %s...done', file_name)
        oss_utils.delete_file(file_name=file_fullname)
        logger.debug('Local file %s...deleted', file_name)

    return current_position


@log_utils.debug_enabled(logger)
def run():
    """ docstring """
    # app.run(host='0.0.0.0') # Dev mode
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
