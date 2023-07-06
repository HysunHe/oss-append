""" Hysun He (hysun.he@oracle.com) @ 2023/07/06 """

import os
import logging
import subprocess
from pathlib import Path
from devlog import my_logger as log_utils

logger = logging.getLogger(__name__)


@log_utils.debug_enabled(logger)
def ensure_file_exists(work_dir: str, file_name: str):
    """ docstring """
    file_fullname = f'{work_dir}/{file_name}'
    if os.path.isfile(file_fullname):
        return  # file already exists

    file_path = Path(file_fullname)
    file_dir = file_path.parent.absolute()
    command = f'mkdir -p {file_dir} && touch {file_fullname}'
    try:
        with log_utils.safe_rich_status(
                f'[bold cyan]Creating file {file_name}[/]'):
            subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as ex:
        logger.error(ex.output)
        with log_utils.print_exception_no_traceback():
            raise IOError(f'Failed to create file {file_name}.') from ex


@log_utils.debug_enabled(logger)
def delete_file(work_dir: str, file_name: str):
    """ docstring """

    file_fullname = f'{work_dir}/{file_name}'
    if not os.path.isfile(file_fullname):
        return  # file already exists

    tmp_dir = file_name
    while True:
        tmp_dir = Path(tmp_dir)
        if str(tmp_dir) in ('.', '~', '/'):
            break

        command = f'rm -rf {work_dir}/{tmp_dir}'
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
