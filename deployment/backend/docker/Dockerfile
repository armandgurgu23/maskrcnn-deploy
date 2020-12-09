FROM python:3.6
WORKDIR /src
# Install the python dependencies inside the spawned containers.
COPY deployment/backend/docker/requirements.txt /src
# Add the application entrypoint to the container.
COPY deployment/backend/docker/appEntrypoint.sh /src
# Copy the source code over into the private filesystem of spawned containers.
COPY src/backend /src/app
# Set up python dependencies and run entrypoint.
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 6969
ENTRYPOINT ["./appEntrypoint.sh"]