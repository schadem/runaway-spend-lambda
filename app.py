import os
from aws_cdk import App, Environment
from runaway_spend_lambda.main import MyStack

# for development, use account/region from cdk cli
dev_env = Environment(
  account=os.getenv('CDK_DEFAULT_ACCOUNT'),
  region=os.getenv('CDK_DEFAULT_REGION')
)

app = App()
MyStack(app, "runaway-spend-lambda-dev", env=dev_env)
# MyStack(app, "runaway-spend-lambda-prod", env=prod_env)

app.synth()