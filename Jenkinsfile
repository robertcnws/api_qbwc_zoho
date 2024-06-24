pipeline {
    agent any
    environment {
        // Define variables de entorno necesarias para tu pipeline
        DOCKER_REGISTRY = 'docker.io'
    }
    stages {
        stage('Setup') {
            agent {
                docker {
                    // Utilizar la imagen de Jenkins para ejecutar este stage
                    image 'jenkins/jenkins:lts'
                    args '-v /var/run/docker.sock:/var/run/docker.sock' // Montar el socket de Docker
                }
            }
            steps {
                script {
                    // Instalar Docker Compose si no está instalado
                    sh 'command -v docker-compose || { curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose; }'
                }
            }
        }
        stage('Build') {
            agent {
                docker {
                    // Utilizar el servicio de Jenkins definido en docker-compose.yml
                    label 'jenkins'
                }
            }
            steps {
                // Construir la imagen de la aplicación Django
                sh 'docker-compose -f docker-compose.yml build'
            }
        }
        stage('Test') {
            agent {
                docker {
                    // Utilizar el servicio de Jenkins definido en docker-compose.yml
                    label 'jenkins'
                }
            }
            steps {
                // Ejecutar pruebas, por ejemplo tests de Django
                sh 'docker-compose -f docker-compose.yml run --rm django-app python manage.py test'
            }
        }
        stage('Deploy') {
            agent {
                docker {
                    // Utilizar el servicio de Jenkins definido en docker-compose.yml
                    label 'jenkins'
                }
            }
            steps {
                // Detener y eliminar contenedores existentes antes de desplegar (opcional)
                sh 'docker-compose -f docker-compose.yml down'

                // Desplegar la aplicación utilizando Docker Compose
                sh 'docker-compose -f docker-compose.yml up -d'
            }
        }
    }
    post {
        always {
            // Limpiar el espacio de trabajo
            cleanWs()
        }
    }
}
