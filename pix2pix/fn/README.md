# Pix2Pix on Fn

## Prerequisites
 * Install Fn: https://fnproject.io/tutorials/install/
 * Make sure your Fn server is running: `sudo fn start`
 * Make sure you have this usecases repo.
 * Make sure you have trained generator_model.h5 from Pix2Pix inside the template directory.

## Deploy Pix2Pix on Fn 
Build the image from the Dockerfile in this directory.

`docker build --no-cache -t fndemo/stacks-fn-pix2pix -f Dockerfile .`

Create the myfunc directory which will be used in the function creation process.

`mkdir myfunc && cd myfunc`

Initialize the function.

`fn init --init-image=fndemo/stacks-fn-pix2pix`

Deploy the function.

`fn deploy --app myfn-app --create-app --local --verbose`

Update the function definition to give it more memory and increase the timeout, since by default it's not enough to run Pix2Pix.

`fn update function myfn-app myfunc --memory 1024 --timeout 90`

Now, lets get the endpoint of our Pix2Pix function we've just created.

`fn inspect function myfn-app myfunc`

You should see something like this.

```
{
        "annotations": {
                "fnproject.io/fn/invokeEndpoint": "http://localhost:8080/invoke/01E4CAMDNPNG8G00GZJ000000X"
        },
        "app_id": "01E4CAMCSNNG8G00GZJ000000W",
        "created_at": "2020-03-26T21:05:40.534Z",
        "id": "01E4CAMDNPNG8G00GZJ000000X",
        "idle_timeout": 30,
        "image": "mysnomer/myfunc:0.0.2",
        "memory": 1024,
        "name": "myfunc",
        "timeout": 90,
        "updated_at": "2020-03-26T21:05:40.558Z"
}
```

Hold on to the value in the fnproject.io/fn/invokeEndpoint field, we're going to need it in the next step.

Use the following command to invoke the Pix2Pix function we've created. Be sure to give it the invokeEndpoint we got from the previous command as well as the path of the image you'd like to input.

`curl -X POST <Your invoke endpoint> --data-binary @<Your input file>`

You should get back a string of base64, which is the base64 encoded output image of the function after inference has been run on your input image. 

Nice, that about wraps it up! If you'd like some more all-in-one sort of commands, read on.

This command will post the image of your choice to the endpoint of the function you've just created and output the image as a base64 string.

`curl -X POST $(fn inspect function myfn-app myfunc | jq -r ".annotations."\"fnproject.io/fn/invokeEndpoint\") --data-binary @<Your image path here>`

If you have JQ installed, this command will send the image of your choice to the endpoint of the function you've just created, decode the base64 output, and write it to output.jpg.

`(curl -X POST $(fn inspect function myfn-app myfunc | jq -r ".annotations."\"fnproject.io/fn/invokeEndpoint\") --data-binary @<Your image path here>) | base64 -d > output.jpg`

There is a build.sh shell script with all of the deployment steps for ease of use. It uses the 0.jpg in this directory as input to the Pix2Pix function.
