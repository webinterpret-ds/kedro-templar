from pathlib import Path
import os

TEMPLATES_DIR = Path('./examples/base')
OUTPUT_DIR = Path("./conf/base")
aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('AWS_DEFAULT_REGION')