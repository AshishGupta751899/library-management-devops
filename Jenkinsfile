pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify') {
            steps {
                sh 'echo "Library Management CI/CD Pipeline"'
                sh 'git --version'
                sh 'docker --version'
                sh 'kubectl version --client'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t library-management:${BUILD_NUMBER} .
                    docker tag library-management:${BUILD_NUMBER} library-management:latest
                '''
            }
        }

        stage('Docker Image Check') {
            steps {
                sh 'docker images | grep library-management'
            }
        }
    }
}