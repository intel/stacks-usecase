import io
import json
from fdk import response
from infer import infer

def handler(ctx, data: io.BytesIO=None):
    outputImage = None
    try:
        # Get the input image as base64
        imageAsBase64String = data.getvalue()
        # Turn the base64 input into a file object
        inputImage = io.BytesIO(imageAsBase64String)
        # Run inference on the image
        outputImage = infer(inputImage)

    except (Exception, ValueError) as ex:
        print(str(ex))

    # Return the output image as an ascii string encoded in base64
    return response.Response(ctx, response_data=str(outputImage, 'ascii'),headers={"Content-Type": "text/html"})
