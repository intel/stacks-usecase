#!/bin/bash

rm -rf myfunc/
fn delete app myfn-app
docker build --no-cache -t fndemo/stacks-fn-pix2pix -f Dockerfile .
mkdir myfunc && cd myfunc && cp ../0.jpg .
fn init --init-image=fndemo/stacks-fn-pix2pix
fn deploy --app myfn-app --create-app --local --verbose
fn update function myfn-app myfunc --memory 1024 --timeout 90
(curl -X POST $(fn inspect function myfn-app myfunc | jq -r ".annotations."\"fnproject.io/fn/invokeEndpoint\") --data-binary @0.jpg) | base64 -d > output.jpg
 
