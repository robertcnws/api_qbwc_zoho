pipeline {
    agent any
    environment {
        // Define variables de entorno necesarias para tu pipeline
        DOCKER_REGISTRY = 'docker.io'
    }
    stages {
        stage('Build') {
            steps {
                script {
                    // Paso para construir la imagen de Django y Nginx
                    sh 'docker-compose build'
                }
            }
        }
        // stage('Test') {
        //     steps {
        //         script {
        //             // Paso para ejecutar pruebas, por ejemplo tests de Django
        //             sh 'docker-compose run --rm django-app python manage.py test'
        //         }
        //     }
        // }
        stage('Deploy') {
            steps {
                script {
                    // Paso para desplegar la aplicación
                    sh 'docker-compose up -d'
                }
            }
        }
    }
    post {
        always {
            // Siempre ejecutar limpieza o acciones adicionales
            cleanWs()
        }
    }
}
