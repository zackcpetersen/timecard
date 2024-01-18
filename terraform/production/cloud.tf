terraform {
  cloud {
    organization = "zackcpetersen"

    workspaces {
      name = "production-cli"
    }
  }
}
