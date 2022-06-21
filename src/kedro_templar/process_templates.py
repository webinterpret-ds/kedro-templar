import logging
import os
from pathlib import Path
from typing import Text, Dict
import boto3
from botocore.exceptions import ClientError
import click
import yaml
from jinja2 import Environment, FileSystemLoader

log = logging.getLogger(__name__)


# settings.py
TEMPLATES_DIR = Path('./examples/base')
OUTPUT_DIR = Path("./conf/base")
aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('AWS_DEFAULT_REGION')

# lib/templates.p
def create_environment(templates_dir: Text) -> Environment:
    """
    Creates an jinja2 environment from provided directory path.
    :param templates_dir: a path to a directory with all templates.
    :returns: a created environment object
    """
    return Environment(
        loader=FileSystemLoader(searchpath=templates_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )


# lib/utils.py
def load_config(config_path: Text) -> Dict:
    """Loads and parases a yaml config into a dict object."""
    return yaml.full_load(open(config_path))


def save_result(result: Text, output_filepath: Path, replace: bool=True):
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


def upload_file_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# main.py
@click.command()
@click.option(
    "-c",
    "--config",
    "config_path",
    required=True,
    type=click.Path(exists=True)
)
@click.option(
    "-t",
    "--templates",
    "templates_dir",
    required=False,
    default=TEMPLATES_DIR,
    type=click.Path(exists=True)
)
@click.option(
    "-o",
    "--output",
    "output_dir",
    required=False,
    default=OUTPUT_DIR,
    type=click.Path(exists=True)
)
@click.option(
    "-f",
    "--force",
    "replace_existing",
    required=False,
    default=False,
    type=bool
)
@click.option(
    "-s",
    "--source",
    "config_source",
    required=False,
    default=False,
    type=bool
)
def process_templates(
    config_path: Text,
    templates_dir: Text,
    output_dir: Text,
    replace_existing: bool,
    config_source: Text
):
    upload_
    config = load_config( config_source if config_source else config_path)
    environment = create_environment(templates_dir)
    for template_path in environment.list_templates():
        template = environment.get_template(template_path)
        result = template.render(config)
        output_path = Path(output_dir) / template_path
        save_result(result, output_path, replace_existing)
    log.info('Filling templates was finished')


if __name__ == "__main__":
    process_templates()
