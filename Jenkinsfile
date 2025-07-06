pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        DJANGO_SETTINGS_MODULE = 'intelligent_LMS.settings' 
    }

    stages {
        stage('Clone') {
            steps {
                echo 'Cloning repository...'
                git 'https://github.com/Rudro5532/Skillup-LMS.git'
            }
        }

        stage('Setup Python & Install Requirements') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/Scripts/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Migrations') {
            steps {
                echo 'Running Django migrations...'
                sh '''
                    . ${VENV_DIR}/Scripts/activate
                    python manage.py migrate
                '''
            }
        }

        stage('Collect Static Files') {
            steps {
                echo 'Collecting static files...'
                sh '''
                    . ${VENV_DIR}/Scripts/activate
                    python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Check Server') {
            steps {
                echo 'Checking Django health...'
                sh '''
                    . ${VENV_DIR}/Scripts/activate
                    python manage.py check
                '''
            }
        }
    }
}
