pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                git 'https://github.com/jaikrgupta/CarthageAPI-1.0.git'
                echo pwd()
                sh 'ls -alrt'
                sh 'pip install -r requirements.txt'
                sh 'python app.py &'
                sleep(5)
            }
        }
        stage('Test') {
            steps {
                sh 'chmod 777 ./scripts/test-script.sh'
                sh './scripts/test-script.sh'
                sh 'cat ./test-reports/test_script.log'
                sleep(5)
            }
        }
        stage('Dockerize') {
            steps {
                sh 'chmod 777 ./scripts/dockerize.sh'
                sh './scripts/dockerize.sh'
                sh 'cat ./test-reports/dockerize.log'
                sleep(5)
            }
        }
        stage('Deployment') {
            steps {
                sh 'chmod 777 ./scripts/heroku.sh'
                sh './scripts/heroku.sh'
                sh 'cat ./test-reports/heroku_deployment.log'
                sleep(5)
            }
        }
    }
}
