resource "aws_eks_cluster" "eks" {
  name     = var.cluster_name
  role_arn = var.cluster_role_arn
  version  = "1.33"

  vpc_config {
    subnet_ids              = var.subnet_ids
    security_group_ids      = [var.security_group_id]
    endpoint_public_access  = true
    endpoint_private_access = false
  }

  depends_on = [
    var.cluster_policy_dependency
  ]

  tags = {
    Name                                    = var.cluster_name
    "alpha.eksctl.io/cluster-oidc-enabled" = "true"
  }
}