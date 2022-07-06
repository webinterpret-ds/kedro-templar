# Kedro Templar 

# About
A plugin build for [Kedro](https://kedro.readthedocs.io/en/stable/) to support templating configuration files.
Using this plugin you can specify a templates for your configuration files such as `catalog.yaml`, `paramters.yaml` 
and fill them automatically using one file with specified variables.
Using this approach you can easily parametrize you pipeline from single point.

Usage examples:
- you can store multiple simultaneous configurations and switch between them on demand.
- change prefixes in `catalog.yaml` to reuse the same pipeline for different data,

## Install
Plugin can be easily installed using pypi repository.
```bash
pip install kedro-templar
```

## Templates
`kedro-templar` is using [jinja2](https://jinja.palletsprojects.com/) templating engine for rendering files.

### Example
#### catalog.yaml
Let's create a template for `conf/base/catalog.yaml` in `templates/base/catalog.yaml`.

```yaml
sample_data:
  type: pandas.CSVDataSet
  save_args:
    index: True
  filepath: s3://your_bucket/{{run_name}}/{{another_subname}}/data/sample_data.csv
```

#### definition.yaml
Your file that contains all variables used for templating.
```yaml
run_name: run_1
another_subname: subfolder
```

#### Render templates
To render created template with provided variables run following command:

```bash
kedro templar apply -c definition.yaml
```

If you choose to have different setup, you can check help command to see all available options:

```bash
kedro templar apply --help
```

## Commands
Currently, this plugin supports 3 commands:
### apply
A core logic of this plugin. This command is used 
to create config files based on provided templates and a file with variables.

You can setup a default values using environment variables:
 - `TEMPLAR_TEMPLATES_DIR` - a default directory for your templates
 - `TEMPLAR_OUTPUT_DIR` - a default directory where templates will be rendered

If no value is specified explicitly and env var is empty,
the commands will use default value specified in the code.

```bash
kedro templar apply -c definition.yaml
```

### download
A helper function used to download a config file from a given S3 path
```bash
kedro templar download -i <S3_PATH>/definition.yaml -o definition.yaml
```

### upload
A helper function used to upload a config file to a given S3 path
```bash
kedro templar upload -i definition.yaml -o <S3_PATH>/definition.yaml
```

# Contact
Plugin was created by the Data Science team from [WebInterpret](https://www.webinterpret.com/).
