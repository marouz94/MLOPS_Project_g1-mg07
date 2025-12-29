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
  }
} 

# Bloc Provider indispensable
provider "aws" {
  region = "eu-west-3"
}

# Création du registre Docker (ECR)
resource "aws_ecr_repository" "api_repo" {
  name                 = "ecr-api-g1mg07"
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

# Le Service App Runner
resource "aws_apprunner_service" "sales_api_service" {
  service_name = "apprunner-g1mg07"

  depends_on = [aws_iam_role_policy_attachment.apprunner_policy_g1mg07]

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_role_g1mg07.arn
    }
    image_repository {
      image_identifier      = "${aws_ecr_repository.api_repo.repository_url}:latest"
      image_repository_type = "ECR"
      image_configuration {
        port = "8000"
      }
    }
    auto_deployments_enabled = true
  }
}

#  Le Rôle IAM spécifique au groupe
resource "aws_iam_role" "apprunner_role_g1mg07" {
  name = "role-apprunner-g1mg07"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = ["build.apprunner.amazonaws.com", "tasks.apprunner.amazonaws.com"]
        }
      },
    ]
  })
}

#  L'attachement des droits de lecture ECR
resource "aws_iam_role_policy_attachment" "apprunner_policy_g1mg07" {
  role       = aws_iam_role.apprunner_role_g1mg07.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

# Output pour ton rapport final
output "app_runner_url" {
  value = aws_apprunner_service.sales_api_service.service_url
}
