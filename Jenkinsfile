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

stage('Push to ECR') {
    steps {
        sh '''
            AWS_REGION="ap-south-1"
            AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
            ECR_REPO="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/library-management"

            aws ecr get-login-password --region ${AWS_REGION} | \
            docker login --username AWS --password-stdin ${ECR_REPO}

            docker tag library-management:${BUILD_NUMBER} ${ECR_REPO}:${BUILD_NUMBER}
            docker tag library-management:${BUILD_NUMBER} ${ECR_REPO}:latest

            docker push ${ECR_REPO}:${BUILD_NUMBER}
            docker push ${ECR_REPO}:latest
        '''
    }
}