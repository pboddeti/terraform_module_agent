variable "project_id" {
  description = "GCP project ID where the bucket will be created"
  type        = string
}

variable "bucket_name" {
  description = "Globally unique GCS bucket name"
  type        = string
}

variable "region" {
  description = "GCP region for the bucket location"
  type        = string
  default     = "us-central1"
}

variable "force_destroy" {
  description = "Delete objects in the bucket when destroying the bucket"
  type        = bool
  default     = false
}
