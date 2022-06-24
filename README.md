# kedro-templar

creates a structure of config based on parameters
example of folder structure is placed in examples folder


to connect to AWS s3 please create a Environment variable
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
using export
eg export AWS_DEFAULT_REGION=eu-west-2

HOW to build plugin:
type in main folder
pip install .


example 
kedro templar process-templates -c './parameters.yaml '

kedro templar download -f 's3://your path in s3/your_configname.yml'
