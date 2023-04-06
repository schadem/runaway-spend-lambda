import os
from aws_cdk import App, Environment
from runaway_spend_lambda.main import RunawayLambda

# for development, use account/region from cdk cli
dev_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                      region=os.getenv('CDK_DEFAULT_REGION'))

app = App()
RunawayLambda(app, "runaway-spend-lambda", env=dev_env)

app.synth()
