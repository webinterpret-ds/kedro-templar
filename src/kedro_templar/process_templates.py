import logging
from pathlib import Path
from typing import Text

import click

from . import settings, templates
from .core import utils

log = logging.getLogger(__name__)


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
    default="templates",
    envvar="TEMPLAR_TEMPLATES_DIR",
    required=True,
    type=click.Path(exists=True)
)
@click.option(
    "-o",
    "--output",
    "output_dir",
    default="conf",
    envvar="TEMPLAR_OUTPUT_DIR",
    required=True,
    type=click.Path(exists=True)
)
@click.option(
    "-f",
    "--force",
    "replace_existing",
    is_flag=True,
    required=False,
    default=False,
    type=bool
)
def apply(
        config_path: Text,
        templates_dir: Text,
        output_dir: Text,
        replace_existing: bool
):
    config = utils.load_config(config_path)
    environment = templates.create_environment(templates_dir)
    for template_path in environment.list_templates():
        template = environment.get_template(template_path)
        result = template.render(config)
        output_path = Path(output_dir) / template_path
        utils.save_result(result, output_path, replace_existing)


@click.command()
@click.option(
    "-i",
    "--input_path",
    "input_path",
    required=True,
    type=str
)
@click.option(
    "-o",
    "--output",
    "output_path",
    required=True,
)
def download(
        input_path: Text,
        output_path: Text
):
    """downloads only file from s3"""
    file_data = utils.download_file_from_s3(input_path)
    with open(output_path, "wb") as f:
        f.write(file_data)


@click.command()
@click.option(
    "-i",
    "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True)
)
@click.option(
    "-o",
    "--output",
    "output_path",
    required=True,
    type=str
)
def upload(
        input_path: Text,
        output_path: Text
):
    utils.upload_file_to_s3(input_path, output_path)
