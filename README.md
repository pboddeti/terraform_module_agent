# Terraform GCS Bucket Module

Reusable Terraform module to create a Google Cloud Storage bucket.

## Module source

Use this repo directly as a module source:

`git::https://github.com/pboddeti/terraform_module_agent.git?ref=main`

For stable usage, prefer a tag such as `?ref=v1.0.0`.

## Inputs

- `project_id` - GCP project ID where the bucket will be created
- `bucket_name` - globally unique bucket name
- `region` - bucket location, default `us-central1`
- `force_destroy` - whether bucket objects should be deleted on destroy, default `false`

## Outputs

- `bucket_name`
- `bucket_id`
- `bucket_url`

## Example usage from another repo

```hcl
terraform {
  required_version = ">= 1.5.0"

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

module "bucket" {
  source = "git::https://github.com/pboddeti/terraform_module_agent.git?ref=main"

  project_id  = var.project_id
  bucket_name = var.bucket_name
  region      = var.region
}
```

## Notes

- This repo is now a Terraform module, not a runnable wrapper project.
- Authentication, backend, and provider configuration should be defined in the calling repo.
- Bucket names must be globally unique.
