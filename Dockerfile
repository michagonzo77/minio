# Use kubiya/base-action-store:stable as the base image.
# This image provides a pre-configured environment for action stores.
FROM kubiya/base-action-store:stable

# Set the working directory to /home/app within the container.
# This directory will contain all the necessary code and files.
WORKDIR /home/app

# Copy the requirements.txt file into the 'function/' directory in the container.
# The requirements.txt should list all Python packages needed for your action store.
COPY requirements.txt function/

# Install the Python packages listed in requirements.txt.
# The '--no-cache' flag ensures that the packages are installed fresh without using any cached versions.
# The '--user' flag installs the packages for the current user, avoiding the need for root permissions.
RUN pip install --no-cache -r function/requirements.txt --user

# Copy all the other source code and files into the 'function/' directory in the container.
# This is to ensure that all your action store code and additional files are present within the container.
COPY . function/

# Install curl to download Helm
RUN apt-get update && apt-get install -y curl

RUN curl https://dl.min.io/client/mc/release/linux-amd64/mc -o /usr/local/bin/mc && \
#Older version: https://dl.min.io/client/mc/release/linux-amd64/archive/mc.RELEASE.2022-12-13T00-23-28Z
    chmod +x /usr/local/bin/mc