FROM python:3.6
WORKDIR /src
# Install the python dependencies inside the spawned containers.
COPY deployment/backend/docker/requirements.txt /src
# Copy the source code over into the private filesystem of spawned containers.
COPY src/backend /src/app
# Set up python dependencies and run entrypoint.
RUN pip3 install -r requirements.txt
EXPOSE 6969
RUN cd /src/app
ENTRYPOINT ["python3", "applicationServer.py"]