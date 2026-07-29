resource "tls_private_key" "jenkins_key" {

  algorithm = "RSA"

  rsa_bits = 4096

}


resource "aws_key_pair" "jenkins_keypair" {

  key_name = "jenkins-key"

  public_key = tls_private_key.jenkins_key.public_key_openssh

}


resource "local_file" "jenkins_pem" {

  content = tls_private_key.jenkins_key.private_key_pem

  filename = "${path.module}/jenkins-key.pem"

}