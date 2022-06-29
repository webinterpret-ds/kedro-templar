import codecs
import os

import setuptools

here = os.path.abspath(os.path.dirname(__file__))


def path_in_project(*path):
    return os.path.join(here, *path)


def read_file(filename):
    with codecs.open(path_in_project(filename)) as f:
        return f.read()


def read_requirements(filename):
    contents = read_file(filename).strip('\n')
    return contents.split('\n') if contents else []


setuptools.setup(
    name='kedro_templar',
    test_suite='tests',
    install_requires=read_requirements('requirements.txt'),
    entry_points={"kedro.project_commands": ["kedro_templar = kedro_templar.plugin:commands"]}
)
