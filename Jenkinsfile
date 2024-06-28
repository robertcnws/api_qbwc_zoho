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
                        // Crear la red si no existe
                        sh '''
                            docker network inspect api_qbwc_zoho_network >/dev/null 2>&1 || docker network create api_qbwc_zoho_network
                        '''

                        // Detener y eliminar contenedores existentes si están en ejecución
                        sh '''
                            docker stop project_api nginx_server || true
                            docker rm project_api nginx_server || true
                        '''

                        // Iniciar los servicios usando docker-compose
                        sh 'docker-compose up -d --no-recreate --no-build nginx django'

                        // Reiniciar Nginx para asegurar que los cambios sean aplicados
                        sh 'docker exec nginx_server nginx -s reload || true'
                    }
                }
            }
        }
    }
}
