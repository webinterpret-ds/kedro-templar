import click
from . import process_templates as pt
import logging

log = logging.getLogger(__name__)


@click.group(name="YML")
def commands():
    """Kedro plugin for filling config templates """
    pass


@commands.group()
@click.pass_obj
def templar(metadata):
    """Run script that fills templates"""
    log.info('Plugin templar finished run')


templar.add_command(pt.apply)
templar.add_command(pt.upload)
templar.add_command(pt.download)