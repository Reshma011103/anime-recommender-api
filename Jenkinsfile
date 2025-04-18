pipeline {
    agent any

    environment {
        IMAGE_NAME = 'anime-recommender'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-username/anime-recommender.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Stop existing container if running
                    sh 'docker rm -f anime-container || true'
                    
                    // Run the new container
                    sh 'docker run -d -p 8501:8501 --name anime-container $IMAGE_NAME'
                }
            }
        }
    }

    post {
        success {
            echo 'Anime Recommender Deployed Successfully 🎉'
        }
        failure {
            echo 'Something went wrong ❌'
        }
    }
}
