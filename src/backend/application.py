import fastapi
from fastapi import FastAPI

# Create the FastAPI application server.
server = FastAPI()


@server.get('/healthcheck')
def healthcheck():
    return "Mask-RCNN deployment server is healthy!"


@server.get('/')
def root():
    return "Welcome to the Mask-RCNN demo deployment example!"
