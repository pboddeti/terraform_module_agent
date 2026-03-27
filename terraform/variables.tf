variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "arctic-rite-403213"
}

variable "bucket_name" {
  description = "Globally unique GCS bucket name"
  type        = string
}

variable "region" {
  description = "GCP region for provider and bucket location"
  type        = string
  default     = "us-central1"
}
