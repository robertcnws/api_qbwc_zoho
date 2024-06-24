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

    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
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

        stage('Deploy') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/') {
                        // Detener servicios
                        sh 'docker stop nginx_server && echo "Contenedor nginx_server detenido." || echo "El contenedor nginx_server no está en ejecución o no existe."'
                        sh 'docker rm -f nginx_server 2>/dev/null || true'
                        sh 'docker stop project_api && echo "Contenedor project_api detenido." || echo "El contenedor project_api no está en ejecución o no existe."'
                        sh 'docker rm -f project_api 2>/dev/null || true'

                        // Iniciar servicios
                        sh 'docker-compose up -d nginx --build'
                    }
                }
            }
        }
    }
}
