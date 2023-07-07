""" Hysun He (hysun.he@oracle.com) @ 2023/07/06 """

import os
import logging
import subprocess
from pathlib import Path
from devlog import my_logger as log_utils

logger = logging.getLogger(__name__)

WORK_DIR = '/var/tmp/ossappend'


def ensure_file_exists(file_name: str):
    """ docstring """
    file_fullname = f'{WORK_DIR}/{file_name}'
    ensure_dir_exists(file_fullname)
    Path(file_fullname).touch()


def ensure_dir_exists(file_fullname: str):
    os.makedirs(name='/tmp/ossappend', exist_ok=True)
    if os.path.isfile(file_fullname):
        return  # file already exists

    file_path = Path(file_fullname)
    file_dir = file_path.parent.absolute()
    os.makedirs(name=file_dir, exist_ok=True)
    

@log_utils.debug_enabled(logger)
def delete_file(file_name: str):
    """ docstring """
    if not os.path.isfile(file_name):
        return  # file not exists
    try:
        os.remove(file_name)
    except OSError:
        pass


@log_utils.debug_enabled(logger)
def delete_path(relative_path: str):
    """ docstring """
    tmp_path = relative_path
    while True:
        tmp_path = Path(tmp_path)
        if str(tmp_path) in ('.', '~', '/'):
            break
        command = f'rm -rf {WORK_DIR}/{tmp_path}'
        try:
            with log_utils.safe_rich_status(
                    f'[bold cyan]Deleting file {relative_path}[/]'):
                subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as ex:
            logger.error(ex.output)
            with log_utils.print_exception_no_traceback():
                raise IOError(
                    f'Failed to delete file {relative_path}.') from ex

        tmp_path = tmp_path.parent


@log_utils.debug_enabled(logger)
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
