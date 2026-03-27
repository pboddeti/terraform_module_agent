terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

resource "google_storage_bucket" "this" {
  name          = var.bucket_name
  project       = var.project_id
  location      = upper(var.region)
  force_destroy = var.force_destroy

  uniform_bucket_level_access = true
}
