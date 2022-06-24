import yaml
import s3fs
import logging
import os
from pathlib import Path
from typing import Text, Dict


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
        output.write(result)


def download_config_from_s3(file_path: Text):
    """Upload a file to an S3 bucket
    """
    s3 = s3fs.S3FileSystem(anon=False)
    log.info(s3.info())
    with s3.open(file_path, 'rb') as f:
        return yaml.full_load(f)


def upload_config_to_s3( path_to_upload):
    """uploading config data to s3
    :param path_to_upload: name of bucket where particular run is stored, c
    """
    s3 = s3fs.S3FileSystem(anon=False)
    with s3.open(path_to_upload, 'wb') as f:
        f.write(yaml.dump(path_to_upload))

