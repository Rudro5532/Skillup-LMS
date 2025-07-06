pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Clone') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/Rudro5532/Skillup-LMS.git'
            }
        }


        stage('Setup Virtual Env & Install Dependencies') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Migrate Database') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    python manage.py migrate
                '''
            }
        }

        stage('Collect Static Files') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Check Django App') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    python manage.py check
                '''
            }
        }
    }
}
