resource "aws_db_subnet_group" "db_subnet_group" {

  name       = "library-db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "library-db-subnet-group"
  }
}


resource "aws_db_instance" "mysql" {

  identifier = "library-db"

  engine = "mysql"
  engine_version = "8.0"

  instance_class = "db.t3.micro"

  allocated_storage = 20
  storage_type = "gp2"

  db_name  = "library_db"
  username = "admin"
  password = "Admin12345"

  storage_encrypted = true

  publicly_accessible = false


  vpc_security_group_ids = [
    var.security_group_id
  ]

  db_subnet_group_name = aws_db_subnet_group.db_subnet_group.name


  backup_retention_period = 0

  skip_final_snapshot = true
  deletion_protection = false


  tags = {
    Name = "library-db"
  }
}