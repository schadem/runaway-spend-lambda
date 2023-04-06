import os
from aws_cdk import Stack
from constructs import Construct
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_iam as iam
import aws_cdk.aws_s3_notifications as s3n
from aws_cdk import (CfnOutput, RemovalPolicy, Stack)


class RunawayLambda(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        script_location = os.path.dirname(__file__)
        s3_upload_prefix = 'input'
        s3_output_prefix = 'output'

        # S3 bucket
        document_bucket = s3.Bucket(self,
                                    "RunawaySpendBucket",
                                    auto_delete_objects=True,
                                    removal_policy=RemovalPolicy.DESTROY)

        # This Lambda function writes a file to the bucket under the s3_output_prefix
        lambda_function = lambda_.DockerImageFunction(
            self,
            "LambdaRunaway",
            code=lambda_.DockerImageCode.from_image_asset(
                os.path.join(script_location, '../lambda/runaway')),
            memory_size=128,
            architecture=lambda_.Architecture.X86_64,
            environment={
                "S3_OUTPUT_BUCKET": document_bucket.bucket_name,
                "S3_OUTPUT_PREFIX": s3_output_prefix,
                "LOG_LEVEL": "DEBUG"
            })

        # Grand Lambda permission to write to S3 bucket
        lambda_function.add_to_role_policy(
            iam.PolicyStatement(actions=['s3:Put*'],
                                resources=[
                                    f"{document_bucket.bucket_arn}",
                                    f"{document_bucket.bucket_arn}/*"
                                ]))

        # Add notification to trigger Lambda when a file is dropped into the bucket
        # HERE IS THE ERROR!
        document_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(lambda_function),  #type: ignore
            #  .----------------.   .----------------.   .----------------.   .----------------.   .----------------.   .----------------.   .----------------.   .----------------.
            # | .--------------. | | .--------------. | | .--------------. | | .--------------. | | .--------------. | | .--------------. | | .--------------. | | .--------------. |
            # | |  _________   | | | |  _______     | | | |  _______     | | | |     ____     | | | |  _______     | | | |              | | | |              | | | |              | |
            # | | |_   ___  |  | | | | |_   __ \    | | | | |_   __ \    | | | |   .'    `.   | | | | |_   __ \    | | | |      _       | | | |      _       | | | |      _       | |
            # | |   | |_  \_|  | | | |   | |__) |   | | | |   | |__) |   | | | |  /  .--.  \  | | | |   | |__) |   | | | |     | |      | | | |     | |      | | | |     | |      | |
            # | |   |  _|  _   | | | |   |  __ /    | | | |   |  __ /    | | | |  | |    | |  | | | |   |  __ /    | | | |     | |      | | | |     | |      | | | |     | |      | |
            # | |  _| |___/ |  | | | |  _| |  \ \_  | | | |  _| |  \ \_  | | | |  \  `--'  /  | | | |  _| |  \ \_  | | | |     | |      | | | |     | |      | | | |     | |      | |
            # | | |_________|  | | | | |____| |___| | | | | |____| |___| | | | |   `.____.'   | | | | |____| |___| | | | |     |_|      | | | |     |_|      | | | |     |_|      | |
            # | |              | | | |              | | | |              | | | |              | | | |              | | | |     (_)      | | | |     (_)      | | | |     (_)      | |
            # | '--------------' | | '--------------' | | '--------------' | | '--------------' | | '--------------' | | '--------------' | | '--------------' | | '--------------' |
            #  '----------------'   '----------------'   '----------------'   '----------------'   '----------------'   '----------------'   '----------------'   '----------------'
            # Forgetting to filter based on a prefix is a mistake
            # and puts the Lambda function into an endless loop, tiggered by the output being written to the same
            # S3 bucket that triggers the function again without filtering on prefix
            ###
            # s3.NotificationKeyFilter(prefix=s3_upload_prefix)
        )

        CfnOutput(
            self,
            "DocumentUploadLocation",
            value=f"s3://{document_bucket.bucket_name}/{s3_upload_prefix}/")

        current_region = Stack.of(self).region
        CfnOutput(
            self,
            'LambdaFunction',
            # https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/runaway-spend-lambda-LambdaRunaway5C674CB2-UFr1bnMj1nek?tab=monitoring
            value=
            f"https://{current_region}.console.aws.amazon.com/lambda/home?region={current_region}#/functions/{lambda_function.function_name}?tab=monitoring"
        )
