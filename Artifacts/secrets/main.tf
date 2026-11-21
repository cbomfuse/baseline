# Reporting database - test fixture for the CBOM ground-truth corpus; the password protects nothing real.
resource "aws_db_instance" "reporting" {
  identifier     = "reporting-db"
  engine         = "postgres"
  instance_class = "db.t3.micro"
  username       = "reporting"
  password       = "wk9fKRG2-rtKoV8G"
}
