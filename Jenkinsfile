pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/Rudro5532/Skillup-LMS.git'
            }
        }

        stage('Build & Run Docker') {
            steps {
                echo 'Running Docker containers...'
                bat 'docker-compose -f lms.yml down'
                bat 'docker-compose -f lms.yml up --build -d'
            }
        }

        stage('Migrate DB') {
            steps {
                echo 'Running migrations inside docker container...'
                bat 'docker-compose -f lms.yml exec web python manage.py migrate'
            }
        }

        stage('Collect Static Files') {
            steps {
                bat 'docker-compose -f lms.yml exec web python manage.py collectstatic --noinput'
            }
        }

        stage('Check Django App') {
            steps {
                bat 'docker-compose -f lms.yml exec web python manage.py check'
            }
        }

        stage('Stop Containers') {
            steps {
                bat 'docker-compose -f lms.yml down'
            }
        }
    }
}
