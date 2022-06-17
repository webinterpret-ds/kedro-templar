import setuptools

setuptools.setup(
    name='kedro_templar',
    test_suite='tests',
    install_requires=[],
    entry_points={"kedro.project_commands": ["templar = kedro_templar.plugin:commands"]}
)
