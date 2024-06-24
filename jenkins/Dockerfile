# Dockerfile for Jenkins
FROM jenkins/jenkins:lts

USER root

# Install Docker
RUN curl -fsSL https://get.docker.com/ | sh

# Allow Jenkins to use Docker
RUN usermod -aG docker jenkins

# RUN apt-get update && apt-get install -y \
#     nginx \
#     python3-pip \
#     && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y curl
RUN curl -L "https://github.com/docker/compose/releases/download/<versión>/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose

USER jenkins
