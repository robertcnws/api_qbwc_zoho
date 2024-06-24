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
                        sh 'docker-compose down -v --remove-orphans nginx'
                        sh 'docker-compose down -v --remove-orphans django'

                        // Iniciar servicios
                        sh 'docker-compose up -d nginx'
                        sh 'docker-compose up -d django'
                    }
                }
            }
        }
    }
}
