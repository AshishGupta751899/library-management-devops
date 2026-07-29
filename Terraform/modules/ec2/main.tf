resource "aws_instance" "jenkins_server" {

  ami = var.ami_id

  instance_type = var.instance_type

  subnet_id = var.subnet_id

  vpc_security_group_ids = [
    var.security_group_id
  ]

  associate_public_ip_address = true


  key_name = var.key_name


  iam_instance_profile = var.instance_profile


  tags = {

    Name = "Jenkins-Server"

  }

}

resource "aws_eip" "jenkins_eip" {
  domain = "vpc"

  tags = {
    Name = "Jenkins-EIP"
  }
}

resource "aws_eip_association" "jenkins_eip_association" {
  instance_id   = aws_instance.jenkins_server.id
  allocation_id = aws_eip.jenkins_eip.id
}