import logging
import os
from pathlib import Path
from typing import Text, Dict
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
    required=False,
    default=settings.TEMPLATES_DIR,
    type=click.Path(exists=True)
)
@click.option(
    "-o",
    "--output",
    "output_dir",
    required=False,
    default=settings.OUTPUT_DIR,
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
    "-e",
    "--export",
    "export_path",
    required=False,
    type=click.Path(exists=True)
)
def apply(
        config_path: Text,
        templates_dir: Text,
        output_dir: Text,
        replace_existing: bool
):
    utils.check_folder_structure()
    config = utils.load_config(config_path)
    environment = templates.create_environment(templates_dir)
    for template_path in environment.list_templates():
        template = environment.get_template(template_path)
        result = template.render(config)
        output_path = Path(output_dir) / template_path
        utils.save_result(result, output_path, replace_existing)


@click.command()
@click.option(
    "-f",
    "--file",
    "config_path",
    required=True,
    type=str
)
@click.option(
    "-o",
    "--output",
    "output_dir",
    required=False,
    default=settings.CONFIG_OUTPUT_DIR,
    type=str #click.Path(exists=True)
)
@click.option(
    "-r",
    "--replace",
    "replace_existing",
    required=False,
    default=True,
    type=bool
)
def download(
        config_path: Text,
        output_dir: Text,
        replace_existing: bool
):
    """downloads only file from s3"""
    utils.check_folder_structure()
    config = utils.download_config_from_s3(config_path)
    utils.save_result(config, Path(output_dir) / Path(os.path.basename(config_path)), replace_existing)


@click.command()
@click.option(
    "-f",
    "--file",
    "output_path",
    required=True,
    type=str
)
@click.option(
    "-c",
    "--config",
    "path_of_config",
    required=False,
    default=settings.DEFAULT_CONFIG,
    type=str
)
def upload(
        output_path: Text,
        path_of_config: Text
):
    utils.upload_config_to_s3(output_path, path_of_config)


if __name__ == "__main__":
    apply()
