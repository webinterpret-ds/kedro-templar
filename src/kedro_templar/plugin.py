import click
import logging
from .process_templates import apply, upload, download

log = logging.getLogger(__name__)


@click.group(name="templar")
def commands():
    """Kedro plugin for filling config templates """
    ...


@commands.group()
@click.pass_obj
def templar(metadata):
    """Run script that fills templates"""
    log.info('Plugin templar finished run')


templar.add_command(apply)
templar.add_command(upload)
templar.add_command(download)