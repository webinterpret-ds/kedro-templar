import click
import process_templates as pt
import logging

log = logging.getLogger(__name__)


@click.group(name="JSON")
def commands():
    """Kedro plugin for printing the pipeline in JSON format"""
    pass


@commands.command()
@click.pass_obj
def templar(metadata):
    """Run script that fills templates"""
    pt.process_templates()
    log.info('Plugin templar finished run')


