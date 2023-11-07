output "db_host" {
  value = aws_db_instance.main_db.address
}

output "db_port" {
  value = aws_db_instance.main_db.port
}
