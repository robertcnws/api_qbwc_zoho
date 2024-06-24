# Dockerfile for Jenkins
FROM jenkins/jenkins:lts

USER root

# Install Docker
RUN curl -fsSL https://get.docker.com/ | sh

# Allow Jenkins to use Docker
RUN usermod -aG docker jenkins

RUN apt-get update && apt-get install -y \
    nginx \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

USER jenkins
