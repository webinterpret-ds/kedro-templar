# Kedro Templar app

# What is it?
Its a app that helps to create folder structure in eg AWS to fill templates,
based on parameters, eg depending on run name.
Example: If you want take parameters from bucket and store it in run_name folder

'''
to_s3:
  type: PartitionedDataSet
  dataset:
    type: pandas.CSVDataSet
    save_args:
      index: True
  path:
    s3://your_buycket/{{your_parameter}}/data/00_input/pandas_partition/
  filename_suffix: '.csv
'''

and add in parameters.yml

'''
run_name: your_run_name
'''

Please check also example folder


to connect to AWS s3 please create a Environment variable /.aws config file
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
using export
eg export AWS_DEFAULT_REGION=eu-west-2



# How to build plugin
type in main folder
pip install .

# How to debug
use same virtual environment as your kedro project, after build you can run
your kedro in Pycharm by setting:
as script path(path to your venv): /home/user_name/path_to_your_venv/bin/kedro
in parameters add: templar download -f s3://your_bucket/your_folder_with_example_config/paremeters.yml

# Before you run
please add these Env variables:

export TEMPLATES_DIR='./templates/base'
export OUTPUT_DIR='./conf/base'
export CONFIG_OUTPUT_DIR='./templates/config'
export DEFAULT_CONFIG='./templates/config/parameters.yml'
