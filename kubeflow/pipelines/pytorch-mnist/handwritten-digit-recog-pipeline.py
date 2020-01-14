# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Pytorch MNIST example running on Kubeflow Pipelines

Run this script to compile pipeline
"""


import kfp.dsl as dsl
import kfp.gcp as gcp

@dsl.pipeline(
  name='dlrs-mnist-pipeline',
  description='A pipeline to train and serve the Pytorch MNIST example.'
)
def mnist_pipeline(model_bucket='your-gs-bucket-name', gcloud_access_token='your-access-token'):
  """
  Pipeline with three stages:
    1. Train a MNIST handwritten digit classifier
    2. Deploy a model server to the cluster
    3. Deploy a web-ui to interact with it
  """
  train = dsl.ContainerOp(
      name='train',
      image='REGISTRY/dlrs-train-TYPE',
      arguments=[
          "-cb", model_bucket,
          "-s", "train",
          "-t", gcloud_access_token
          ]
  )

  serve = dsl.ContainerOp(
      name='serve',
      image='REGISTRY/dlrs-pipelines-deployer',
      arguments=[
          "-cb", model_bucket,
          "-s", "serve",
          "-t", gcloud_access_token
          ]
  )
  serve.after(train)

  web_ui = dsl.ContainerOp(
      name='web-ui',
      image='REGISTRY/dlrs-pipelines-deployer'
      arguments=[
          "-s", "website"
          ]
  )
  web_ui.after(serve)

  steps = [train, serve, web_ui]
  for step in steps:
    step.apply(gcp.use_gcp_secret('user-gcp-sa'))

if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(mnist_pipeline, __file__ + '.tar.gz')
