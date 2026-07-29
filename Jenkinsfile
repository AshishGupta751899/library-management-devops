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
    }
}