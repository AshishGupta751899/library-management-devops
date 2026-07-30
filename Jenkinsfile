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
                sh 'aws --version'
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

        stage('Push to ECR') {
            steps {
                sh '''
                    AWS_REGION="ap-south-1"
                    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
                    ECR_REPO="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/library-management"

                    echo "ECR Repository: ${ECR_REPO}"

                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin ${ECR_REPO}

                    docker tag library-management:${BUILD_NUMBER} ${ECR_REPO}:${BUILD_NUMBER}
                    docker tag library-management:${BUILD_NUMBER} ${ECR_REPO}:latest

                    docker push ${ECR_REPO}:${BUILD_NUMBER}
                    docker push ${ECR_REPO}:latest
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                    aws eks update-kubeconfig --region ap-south-1 --name library-eks

                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/configmap.yaml
                    kubectl apply -f k8s/secret.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl apply -f k8s/ingress.yaml

                    kubectl rollout status deployment/library-management -n library

                    kubectl get pods -n library
                    kubectl get svc -n library
                    kubectl get ingress -n library
                '''
            }
        }

    }
}