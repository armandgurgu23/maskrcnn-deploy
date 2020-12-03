import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from modelServer import ModelServer
import logging
import uvicorn
import argparse

# Create the FastAPI application server.
server = FastAPI()


def getApplicationLogger():
    # We use the built-in uvicorn logger that comes
    # out of the box when setting up a FastAPI
    # server.
    return logging.getLogger("uvicorn.info")


# A list of all the front-end origins that are allowed to access the server.
# We choose them depending on the development mode flag:


def fetchServerAllowedOrigins():
    if os.environ['SERVER_MODE'] == 'dev':
        # In dev mode we only allow localhost connections!
        # to-do: the front-end endpoint has to be
        # exposed to back-end to allow it as
        # an origin.
        # Alternatively, find a way to expose
        # all localhost port numbers in dev mode.
        allowedOrigins = ['http://localhost:3000']
    else:
        allowedOrigins = ['*']
    return allowedOrigins


def setupCORSMiddleware(server):
    allowedOrigins = fetchServerAllowedOrigins()
    # Can specify certain types of HTTP methods to allow (ie: just POST/GET etc.)
    # As well as different credentials like authorization headers/cookies etc.
    # Same applies for HTTP headers.
    applicationLogger.info(
        'Origins allowed to access backend: {}'.format(allowedOrigins))
    server.add_middleware(CORSMiddleware, allow_origins=allowedOrigins,
                          allow_credentials=True,
                          allow_methods=["*"],
                          allow_headers=["*"])
    return


@server.get('/healthcheck')
def healthcheck():
    # From experimentation, we cannot test the uploadImage functionality
    # until we set up an HTML form that can be used to upload images/files
    # In the HTML form, the action parameter refers to the URL where
    # the content is processed?!?!?!
    htmlContent = """
<body>
<h1> Welcome to the Mask-RCNN demo backend server! </h1>
<h2> Mask-RCNN deployed backend server is healthy! </h2>
</body>
    """
    return HTMLResponse(htmlContent)


@server.get('/')
def root():
    return RedirectResponse('/healthcheck')


# Note from Armand: You do NOT need the frontend code for now to test the backend.
# You can just go to /docs and test out uploadImage using the SwaggerUI
# interface for now.
# TO DO: Figure out how to return an image using Fast API.
# (The returned image will be the image with the drawn predictions)!


@server.post('/detector')
def runObjectDetector(imageFile: UploadFile = File(...)):
    applicationLogger.info('Handling a detector request!')
    imageExtension = imageFile.content_type.split('/')[-1]
    predictionsImage = modelService(imageFile.file, imageExtension, 'detector')
    return StreamingResponse(predictionsImage, media_type=imageFile.content_type)


@server.post('/segmentor')
def runObjectSegmentor(imageFile: UploadFile = File(...)):
    applicationLogger.info('Handling a segmentor request!')
    imageExtension = imageFile.content_type.split('/')[-1]
    predictionsImage = modelService(
        imageFile.file, imageExtension, 'segmentor')
    return StreamingResponse(predictionsImage, media_type=imageFile.content_type)


def getApplicationStartUpArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", type=str, help="The URL of the application host. Defaults to localhost.", default="localhost")
    parser.add_argument(
        "--port", type=int, help="The host server machine port to run the application on.", default=6969)
    args = parser.parse_args()
    return args

# TO-DO (debug): For some reason moving these global variables under
# name == main causes them to not be accessible within FastAPIs routes
# However these global variables are initialized twice in here
# compared to once under the name == main block.


modelService = ModelServer()
applicationLogger = getApplicationLogger()
setupCORSMiddleware(server)
applicationArgs = getApplicationStartUpArgs()


if __name__ == "__main__":
    uvicorn.run("applicationServer:server", host=applicationArgs.host,
                port=applicationArgs.port)
