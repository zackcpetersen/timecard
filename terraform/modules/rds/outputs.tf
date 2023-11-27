output "db_host" {
  value = aws_db_instance.main_db.address
}

output "db_port" {
  value = aws_db_instance.main_db.port
}

output "db_name" {
  value = aws_db_instance.main_db.db_name
}

output "db_user" {
  value = aws_db_instance.main_db.username
}
