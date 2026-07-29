variable "aws_region" {
  description = "AWS Region where resources will be created"
  type        = string
}



variable "jenkins_ami_id" {
  description = "Ubuntu AMI ID for Jenkins EC2"
  type        = string
}


variable "jenkins_instance_type" {
  description = "EC2 instance type for Jenkins"
  type        = string
  default     = "t2.medium"
}
