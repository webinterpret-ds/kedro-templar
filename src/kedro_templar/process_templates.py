import logging
import os
from pathlib import Path
from typing import Text, Dict
import click
import settings,  templates
from lib import utils
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
def process_templates(
    config_path: Text,
    templates_dir: Text,
    output_dir: Text,
    replace_existing: bool,
    export_path: Text
):
    # extend -c to accept also s3 path, @WOJTEK what do you think?
    if str(config_path).startswith('s3://'):
        config = utils.download_config_from_s3(config_path)
    else:
        config = utils.load_config(config_path)
    environment = templates.create_environment(templates_dir)
    for template_path in environment.list_templates():
        template = environment.get_template(template_path)
        result = template.render(config)
        output_path = Path(output_dir) / template_path
        utils.save_result(result, output_path, replace_existing)
    if not export_path:
        export_path = utils.get_path(config)
    utils.upload_config_to_s3(export_path, config)


if __name__ == "__main__":
    process_templates()
