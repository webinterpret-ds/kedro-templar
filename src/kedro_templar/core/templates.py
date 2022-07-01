from jinja2 import Environment, FileSystemLoader
from typing import Text


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
