pipeline {
    agent any

    // triggers {
    //     pollSCM('* * * * *') // Esto configurará Jenkins para que revise el repositorio cada minuto (cambiar según necesites)
    // }

    triggers {
        githubPush()
    }

    environment {
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
        DOCKER_USER = 'robertcnws'
        DOCKER_REPO = 'robertcnws/api_qbwc_zoho'

    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_USER}:${DOCKER_CREDENTIALS}") {
                        def app = docker.build("${DOCKER_REPO}:latest")
                        app.push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS) {
                        sh 'docker-compose up -d' 
                    }
                }
            }
        }
    }
}
