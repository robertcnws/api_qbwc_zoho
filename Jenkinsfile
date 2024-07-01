pipeline {
    agent any

    // triggers {
    //     pollSCM('* * * * *') // Esto configurará Jenkins para que revise el repositorio cada minuto (cambiar según necesites)
    // }

    triggers {
        githubPush()
    }

    environment {
        DOCKER_CREDENTIALS = credentials('docker-hub-token')
        DOCKER_USER = 'robertocnws'
        DOCKER_REPO = 'robertocnws/api_qbwc_zoho'
        CONTAINER_NAME = 'project_api'
        REPO_URL = 'https://github.com/robertcnws/api_qbwc_zoho.git'

    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'dev', url: "${REPO_URL}"
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    sh """
                        echo \$DOCKER_CREDENTIALS | docker login -u \$DOCKER_USER --password-stdin
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Si el Dockerfile está en un subdirectorio
                    dockerImage = docker.build("${DOCKER_REPO}:${env.BUILD_NUMBER}", '-f project_api/Dockerfile .')
                    dockerImage = docker.build("${DOCKER_REPO}:latest", '-f project_api/Dockerfile .')
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CREDENTIALS}") {
                        dockerImage.push("${env.BUILD_NUMBER}")
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${DOCKER_REPO}:latest
                    """
                }
            }
        }
    }
}
