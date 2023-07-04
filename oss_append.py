""" Hysun He (hysun.he@oracle.com) @ 2023/07/04 """

import logging
import os
import subprocess
import base64

from pathlib import Path
from flask import Flask, request
from devlog import my_logger as log_utils

from oci_config import OciConf as oci_conf

logger = logging.getLogger(__name__)
app = Flask(__name__)

_WORK_DIR = '/var/tmp/ossappend'


@app.route('/write-json', methods=['POST'])
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
    logger.debug('Got requested data: %s', data)

    bucket = data['bucket']
    file_name = data['name']
    file_fullname = f'{_WORK_DIR}/{file_name}'
    # destination = file_name if 'destination' not in data or not data[
    #     'destination'] else data['destination']
    destination = file_name
    file_position = int('0' if 'position' not in data else data['position'])
    whence = 2 if 'position' not in data or file_position < 0 else 0
    content_base64 = data['content']
    append = data['append']
    content_bytes = base64.b64decode(content_base64)

    ensure_file_exists(file_fullname)

    pos = handle_content(file_fullname=file_fullname,
                         file_name=file_name,
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
    file_fullname = f'{_WORK_DIR}/{file_name}'
    append = request.args.get('append')
    file_position = int('0' if not request.args.get('position') else request.
                        args.get('position'))
    # destination = file_name if not request.args.get(
    #     'destination') else request.args.get('destination')
    destination = file_name
    whence = 2 if not request.args.get('position') or file_position < 0 else 0
    logger.debug('file_name: %s', file_name)
    logger.debug('file_position: %d, %d', file_position, whence)
    logger.debug('data: %s', content_bytes)
    logger.debug('append: %s', append)

    ensure_file_exists(file_fullname)

    pos = handle_content(file_fullname=file_fullname,
                         file_name=file_name,
                         file_position=file_position,
                         whence=whence,
                         content_bytes=content_bytes,
                         append=append,
                         bucket=bucket,
                         destination=destination)

    location = f'https://objectstorage.{oci_conf.get_region()}.oraclecloud.com/n/{oci_conf.get_namespace()}/b/{bucket}/o/{file_name}' if append and str(
        append).lower() not in ('true', '1') else ''
    return {'status': 'ok', 'current_file_position': pos, 'location': location}


def ensure_file_exists(file_name):
    """ docstring """
    if os.path.isfile(file_name):
        return  # file already exists

    file_path = Path(file_name)
    file_dir = file_path.parent.absolute()
    command = f'mkdir -p {file_dir} && touch {file_name}'
    try:
        with log_utils.safe_rich_status(
                f'[bold cyan]Creating file {file_name}[/]'):
            subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as ex:
        logger.error(ex.output)
        with log_utils.print_exception_no_traceback():
            raise IOError(f'Failed to create file {file_name}.') from ex


# pylint: disable=too-many-arguments
def handle_content(file_fullname, file_name, file_position, whence,
                   content_bytes, append, bucket, destination) -> int:
    """ docstring """
    current_position = 0
    with open(file_fullname, 'rb+') as dest_file:
        logger.debug('Write content to file. file_position: %d, %d',
                     file_position, whence)
        dest_file.seek(0 if file_position < 0 else file_position, whence)
        dest_file.write(content_bytes)
        current_position = dest_file.tell()

    if append and str(append).lower() not in ('true', '1'):
        logger.debug('Upload file %s...', file_name)
        sync_object_storage(bucket, file_fullname, destination)
        logger.debug('Upload file %s...done', file_name)
        delete_file(file_fullname=file_fullname, file_name=file_name)
        logger.debug('Local file %s...deleted', file_name)

    return current_position


def delete_file(file_fullname, file_name):
    """ docstring """
    if not os.path.isfile(file_fullname):
        return  # file already exists

    tmp_dir = file_name
    while True:
        tmp_dir = Path(tmp_dir)
        if str(tmp_dir) in ('.', '~', '/'):
            break

        command = f'rm -rf {_WORK_DIR}/{tmp_dir}'
        try:
            with log_utils.safe_rich_status(
                    f'[bold cyan]Deleting file {file_name}[/]'):
                subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as ex:
            logger.error(ex.output)
            with log_utils.print_exception_no_traceback():
                raise IOError(f'Failed to delete file {file_name}.') from ex

        tmp_dir_parent = tmp_dir.parent
        tmp_dir = tmp_dir_parent


def sync_object_storage(bucket_name: str, src_file: str, dest_file: str):
    """Upload a file to OCI Object Storage."""

    oci_cli_init = ['export OCI_CLI_SUPPRESS_FILE_PERMISSIONS_WARNING=True']

    upload_via_ocicli = (f'oci os object put --bucket-name {bucket_name} '
                         f'--name "{dest_file}" --file "{src_file}" --force')

    commands = list(oci_cli_init)
    commands.append(upload_via_ocicli)
    commands_string = ' && '.join(commands)

    try:
        with log_utils.safe_rich_status(
                f'[bold cyan]Uploading file {src_file}[/]'):
            subprocess.check_output(commands_string, shell=True)
    except subprocess.CalledProcessError as ex:
        logger.error(ex.output)
        with log_utils.print_exception_no_traceback():
            raise IOError(f'Failed to upload file {src_file}.') from ex


def main():
    """ docstring """
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
