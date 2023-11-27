terraform {
  cloud {
    organization = "zackcpetersen"

    workspaces {
      name = "staging-cli"
    }
  }

  # TODO is this required?
  #  required_providers {
  #    aws = {
  #      source  = "hashicorp/aws"
  #      version = "~> 5.24.0"
  #    }
  #  }
  #
  #  required_version = ">= 1.6.3"
}
