# EKS Cluster Role
resource "aws_iam_role" "eks_cluster_role" {
  name = "library-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "cluster_policy" {
  role       = aws_iam_role.eks_cluster_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

# Node Group Role
resource "aws_iam_role" "eks_node_role" {
  name = "library-eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "worker_node_policy" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "cni_policy" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "ecr_readonly" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# Jenkins EC2 Role
resource "aws_iam_role" "jenkins_role" {
  name = "library-jenkins-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "ec2.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "jenkins_eks_describe" {
  name = "jenkins-eks-describe"
  role = aws_iam_role.jenkins_role.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "eks:DescribeCluster"
        ]

        Resource = "arn:aws:eks:ap-south-1:257076674897:cluster/library-eks"
      }
    ]
  })
}


# ECR Access
resource "aws_iam_role_policy_attachment" "jenkins_ecr" {
  role = aws_iam_role.jenkins_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess"
}


# EKS Access
resource "aws_iam_role_policy_attachment" "jenkins_eks" {
  role = aws_iam_role.jenkins_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}


# EC2 Instance Profile
resource "aws_iam_instance_profile" "jenkins_profile" {
  name = "library-jenkins-profile"

  role = aws_iam_role.jenkins_role.name
}