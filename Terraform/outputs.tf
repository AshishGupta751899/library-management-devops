output "vpc_id" {
  value = module.vpc.vpc_id
}

output "vpc_cidr" {
  value = module.vpc.vpc_cidr
}

output "db_endpoint" {
  value = module.rds.db_endpoint
}

output "jenkins_elastic_ip" {
  value = module.jenkins_ec2.elastic_ip
}

output "jenkins_instance_id" {
  value = module.jenkins_ec2.instance_id
}


