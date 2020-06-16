terraform {
  backend "remote" {
    organization = "loci"
    workspaces {
      name = "dggs"
    }
  }
}

