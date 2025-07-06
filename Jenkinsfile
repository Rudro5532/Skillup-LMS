pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Rudro5532/Skillup-LMS.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t skillup-lms .'
            }
        }

        stage('Run Docker Compose') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }

        stage('Check Running Containers') {
            steps {
                sh 'docker ps'
            }
        }
    }
}
