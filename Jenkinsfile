pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_CREDENTIALS = credentials('docker-hub-token')  // ID de credenciales de tipo Secret text para Docker Hub PAT
        DOCKER_USER = 'robertocnws'  // Tu nombre de usuario en Docker Hub
        DOCKER_REPO = 'robertocnws/api_qbwc_zoho'  // Nombre de tu repositorio en Docker Hub
        CONTAINER_NAME = 'project_api'  // Nombre del contenedor Docker
        REPO_URL = 'https://github.com/robertcnws/api_qbwc_zoho.git'  // URL del repositorio de GitHub
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'dev', url: "${REPO_URL}"  // Reemplaza 'dev' con la rama correcta si es necesario
            }
        }

        // stage('Login to Docker Hub') {
        //     steps {
        //         script {
        //             // Login a Docker Hub usando el PAT (Token de Acceso Personal) como password stdin
        //             sh """
        //                 echo \$DOCKER_CREDENTIALS | docker login -u \$DOCKER_USER --password-stdin
        //             """
        //         }
        //     }
        // }

        stage('Build Docker Image') {
            steps {
                script {
                    // Construye la imagen Docker usando el Dockerfile en el subdirectorio project_api
                    dockerImage = docker.build("${DOCKER_REPO}:${env.BUILD_NUMBER}", '-f project_api/Dockerfile.jenkins .')
                    dockerImage = docker.build("${DOCKER_REPO}:latest", '-f project_api/Dockerfile.jenkins .')
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'docker-hub-token', variable: 'DOCKER_HUB_TOKEN')]) {
                        sh 'echo $DOCKER_HUB_TOKEN | docker login -u robertocnws --password-stdin https://index.docker.io/v1/'
                        sh 'docker push ${DOCKER_REPO}:${IMAGE_TAG}'
                    }
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    sh """
                    docker stop ${CONTAINER_NAME} || true  // Detiene el contenedor si está en ejecución
                    docker rm ${CONTAINER_NAME} || true  // Elimina el contenedor detenido
                    docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${DOCKER_REPO}:latest  // Ejecuta el contenedor en segundo plano
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()  // Limpia el espacio de trabajo después de cada build
        }
    }
}
