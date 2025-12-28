terraform {
required_version = ">= 1.5.0"
required_providers {
   aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
   }
}
# Configuration du backend S3 pour stocker le state
backend "s3" {
   bucket  = "infrastats-g1mg07"
   key     = "g1mg07.tfstate"
   region  = "eu-west-3"
   encrypt = true
} }

# Bloc Provider indispensable
provider "aws" {
  region = "eu-west-3"
}

# Création du registre Docker (ECR)
resource "aws_ecr_repository" "api_repo" {
  name                 = "ecr-g1mg07"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Output pour récupérer l'URL du registre
output "ecr_repository_url" {
  value = aws_ecr_repository.api_repo.repository_url
}
