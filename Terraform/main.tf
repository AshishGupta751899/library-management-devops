module "vpc" {
  source = "./modules/vpc"

  vpc_cidr = "10.0.0.0/16"
  vpc_name = "library-vpc"
}

module "subnet" {
  source = "./modules/subnet"

  vpc_id = module.vpc.vpc_id

  public_subnet_1_cidr = "10.0.1.0/24"
  public_subnet_2_cidr = "10.0.2.0/24"

  private_subnet_1_cidr = "10.0.3.0/24"
  private_subnet_2_cidr = "10.0.4.0/24"

  az_1 = "ap-south-1a"
  az_2 = "ap-south-1b"
}
module "igw" {
  source = "./modules/igw"

  vpc_id = module.vpc.vpc_id
}


module "eip" {
  source = "./modules/eip"
}

module "nat" {
  source = "./modules/nat"

  allocation_id = module.eip.eip_allocation_id
  subnet_id     = module.subnet.public_subnet_1_id

  igw_dependency = module.igw.igw_id
}

module "route_table" {
  source = "./modules/route-table"

  vpc_id = module.vpc.vpc_id

  igw_id         = module.igw.igw_id
  nat_gateway_id = module.nat.nat_gateway_id

  public_subnet_1_id  = module.subnet.public_subnet_1_id
  public_subnet_2_id  = module.subnet.public_subnet_2_id
  private_subnet_1_id = module.subnet.private_subnet_1_id
  private_subnet_2_id = module.subnet.private_subnet_2_id
}

module "security_group" {
  source = "./modules/security-group"

  vpc_id = module.vpc.vpc_id
}

module "iam" {
  source = "./modules/iam"
}

module "ecr" {
  source = "./modules/ecr"

  repository_name = "library-management"
}


module "eks" {
  source = "./modules/eks"

  cluster_name     = "library-eks"
  cluster_role_arn = module.iam.eks_cluster_role_arn

  subnet_ids = [
    module.subnet.private_subnet_1_id,
    module.subnet.private_subnet_2_id
  ]

  security_group_id = module.security_group.eks_sg_id

  cluster_policy_dependency = module.iam.eks_cluster_role_arn
}


module "node_group" {
  source = "./modules/node-group"

  cluster_name    = module.eks.cluster_name
  node_group_name = "library-node-group"

  node_role_arn = module.iam.eks_node_role_arn

  subnet_ids = [
    module.subnet.private_subnet_1_id,
    module.subnet.private_subnet_2_id
  ]

  node_role_dependency = module.iam.eks_node_role_arn
}

module "rds" {
  source = "./modules/rds"

  subnet_ids        = module.subnet.private_subnet_ids
  security_group_id = module.security_group.rds_sg_id
}


module "jenkins_ec2" {
  source = "./modules/ec2"

  ami_id        = var.jenkins_ami_id
  instance_type = var.jenkins_instance_type

  subnet_id = module.subnet.public_subnet_1_id

  security_group_id = module.security_group.jenkins_sg_id

  instance_profile = module.iam.jenkins_instance_profile_name

  key_name = aws_key_pair.jenkins_keypair.key_name
}