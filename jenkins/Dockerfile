# Dockerfile for Jenkins
FROM jenkins/jenkins:lts

# Instalar Docker dentro del contenedor de Jenkins
USER root

RUN apt-get update && \
    apt-get -y install apt-transport-https \
                       ca-certificates \
                       curl \
                       gnupg2 \
                       software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get -y install docker-ce-cli

# Crea el grupo 'docker' si no existe
RUN groupadd -g 1001 docker

# Crear un usuario Jenkins y agregarlo al grupo Docker
RUN usermod -aG docker jenkins

USER jenkins
