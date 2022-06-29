import setuptools


setuptools.setup(
    name='kedro_templar',
    test_suite='tests',
    install_requires=[],
    entry_points={"kedro.project_commands": ["kedro_templar = kedro_templar.plugin:commands"]}
)
