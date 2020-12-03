FROM python:3.6
WORKDIR /src/app
# Install the python dependencies inside the spawned containers.
COPY requirements.txt /src/
RUN cd /src/
RUN pip3 install -r requirements.txt
# Copy the source code over into the private filesystem of spawned containers.
COPY ../../../src/backend/ /src/app/
EXPOSE 6969
RUN cd /src/app
ENTRYPOINT ["python3", "applicationServer.py"]