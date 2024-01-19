terraform {
  cloud {
    organization = "zackcpetersen"

    workspaces {
      name = "copyS3-cli"
    }
  }
}
