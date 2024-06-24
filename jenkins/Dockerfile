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

# Instalar Docker Compose
USER root
RUN curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Instalar Docker CLI (opcional, si no está presente en la imagen base)
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io

USER jenkins
