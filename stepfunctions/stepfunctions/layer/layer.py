import aws_cdk as cdk
import os
from constructs import Construct
from aws_cdk import (
    aws_s3_assets as assets,
    aws_lambda as lambda_,
)


class Layer(Construct):
    layer_version: lambda_.ILayerVersion
    layer_version_arn: str

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        architecture: lambda_.Architecture,
        runtime: lambda_.Runtime,
        path: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f"architecture {architecture}")
        print(f"runtime {runtime}")

        default_platform_flag = os.environ.get("DOCKER_DEFAULT_PLATFORM")
        print(f"DOCKER_DEFAULT_PLATFORM={default_platform_flag}")

        layer_assets = assets.Asset(
            self,
            "LayerAsset",
            path=path,
            bundling=cdk.BundlingOptions(
                image=runtime.bundling_image,
                platform=architecture.docker_platform,
                output_type=cdk.BundlingOutput.AUTO_DISCOVER,
                security_opt="no-new-privileges:true",  # https://docs.docker.com/engine/reference/commandline/run/#optional-security-options---security-opt
                network="host",
                command=[
                    "bash",
                    "-c",
                    "pip install -r requirements.txt -t /asset-output/python && cp -au . /asset-output/python",
                ],
            ),
        )

        layer = lambda_.LayerVersion(
            self,
            "Layer",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            code=lambda_.Code.from_bucket(
                bucket=layer_assets.bucket, key=layer_assets.s3_object_key
            ),
            compatible_architectures=[architecture],
        )

        self.layer_version = layer
        self.layer_version_arn = layer.layer_version_arn
