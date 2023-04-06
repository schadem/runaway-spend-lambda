import json
import logging
import os
import boto3
import time

from datetime import datetime

logger = logging.getLogger(__name__)
s3 = boto3.client('s3')


def lambda_handler(event, _):
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    logger.setLevel(log_level)
    logger.info(json.dumps(event))
    logger.info(f"boto3 version: {boto3.__version__}")

    s3_output_bucket = os.environ.get('S3_OUTPUT_BUCKET', 'somebucket')
    s3_output_prefix = os.environ.get('S3_OUTPUT_PREFIX', 'output')

    logger.debug(f"LOG_LEVEL: {log_level}")

    file_content = {"bla": "foo"}

    output_bucket_key = s3_output_prefix + "/" + "iamafile.txt" + datetime.utcnow(
    ).isoformat() + ".json"
    # we add the sleep to show the concept, but not go crazy
    time.sleep(1)
    s3.put_object(Body=bytes(
        json.dumps(file_content, indent=4).encode('UTF-8')),
                  Bucket=s3_output_bucket,
                  Key=output_bucket_key)
    logger.debug(f"Put object to S3.")
