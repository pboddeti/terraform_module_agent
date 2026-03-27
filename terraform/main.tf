terraform {
  required_version = ">= 1.5.0"

  backend "local" {}

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "this" {
  name          = var.bucket_name
  location      = upper(var.region)
  force_destroy = false

  uniform_bucket_level_access = true
}
