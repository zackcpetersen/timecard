terraform {
  cloud {
    organization = "zackcpetersen"

    workspaces {
      name = "staging-cli"
    }
  }
}
