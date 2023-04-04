from projen.awscdk import AwsCdkPythonApp

project = AwsCdkPythonApp(
    author_email="45048633+schadem@users.noreply.github.com",
    author_name="Martin Schade",
    cdk_version="2.1.0",
    module_name="runaway_spend_lambda",
    name="runaway-spend-lambda",
    version="0.1.0",
)

project.synth()