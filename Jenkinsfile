pipeline {
    agent any

    environment {
        IMAGE_NAME = 'anime-recommender'
        CONTAINER_NAME = 'anime-container'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    bat 'docker build -t %IMAGE_NAME% .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    bat 'docker rm -f %CONTAINER_NAME% || exit 0'
                    bat 'docker run -d -p 8501:8501 --name %CONTAINER_NAME% %IMAGE_NAME%'
                }
            }
        }
    }

    post {
        success {
            echo '✅ Anime Recommender Deployed Successfully!'
        }
        failure {
            echo '❌ Something went wrong.'
        }
    }
}
