import fastapi
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from modelServer import ModelServer
# Create the FastAPI application server.
server = FastAPI()
modelService = ModelServer()


@server.get('/healthcheck')
def healthcheck():
    return "Mask-RCNN deployment server is healthy!"


@server.get('/')
def root():
    # From experimentation, we cannot test the uploadImage functionality
    # until we set up an HTML form that can be used to upload images/files
    # In the HTML form, the action parameter refers to the URL where
    # the content is processed?!?!?!
    htmlContent = """
<body>
<h1> Welcome to the Mask-RCNN demo deployment example! </h1>
</body>
    """
    return HTMLResponse(htmlContent)


# Note from Armand: You do NOT need the frontend code for now to test the backend.
# You can just go to /docs and test out uploadImage using the SwaggerUI
# interface for now.
# TO DO: Figure out how to return an image using Fast API.
# (The returned image will be the image with the drawn predictions)!


@server.post('/uploadImage/')
def uploadImage(imageFile: UploadFile = File(...)):
    # print('Executing the POST method: uploadImage!')
    # print('Can I see the model: {}'.format(modelService))
    predictionsImage = modelService(imageFile.file)
    return {'imageUploaded': imageFile.filename, 'contentType': imageFile.content_type}
