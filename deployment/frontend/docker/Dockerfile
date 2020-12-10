FROM node:12.20-alpine
WORKDIR /src
# Add the application entrypoint to the container.
COPY deployment/frontend/docker/appEntrypoint.sh /src
# Copy the source code over into the private filesystem of spawned containers.
COPY src/frontend /src/app
# Install all the node dependencies.
WORKDIR /src/app
RUN npm install
EXPOSE 3000
ENTRYPOINT ["../appEntrypoint.sh"]