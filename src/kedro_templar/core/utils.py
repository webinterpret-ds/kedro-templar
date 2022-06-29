import yaml
import s3fs
import logging
import os
from pathlib import Path
from typing import Text, Dict
from ..import settings


log = logging.getLogger(__name__)


def load_config(config_path: Text) -> Dict:
    """Loads and parases a yaml config into a dict object."""
    return yaml.full_load(open(config_path))


def save_result(result: Text, output_filepath: Path, replace: bool = True):
    """
    Saves rendered config into an output file.

    :param result: a rendered template in a text format
    :param output_filepath: a filepath where the output will be saved
    :param replace: if set to False, it will only replace the
                    existing file if it doesn't already exist.
    """
    if not replace and output_filepath.exists():
        log.error(f"Skipping saving a file. {output_filepath} already exists!")
        return

    if not os.path.exists(output_filepath.parent):
        log.info(f"Parent directory not found. Creating {output_filepath.parent}.")
        os.makedirs(output_filepath.parent)

    with open(output_filepath, "w") as output:
        if isinstance(result, str):
            output.write(result)
        else:
            output.write(yaml.dump(result))
        log.info('Output saved to '+ str(output_filepath))


def download_file_from_s3(file_path: Text):
    """
    Upload a file to an S3 bucket
    :param file_path: an S3 path to a file
    :returns: content of the downloaded file
    """
    s3 = s3fs.S3FileSystem(anon=False)
    with s3.open(file_path, 'rb') as f:
        return f.read()


def upload_file_to_s3(input_path: Text, output_path: Text):
    """
    Uploading a file data to s3
    :param input_path: input file that will be uploaded
    :param output_path: an S3 path where the fill will be saved
    """
    s3 = s3fs.S3FileSystem(anon=False)
    with s3.open(output_path, 'w') as f:
        f.write(open(input_path).read())
