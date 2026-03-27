output "bucket_name" {
  description = "Created bucket name"
  value       = google_storage_bucket.this.name
}

output "bucket_id" {
  description = "Created bucket ID"
  value       = google_storage_bucket.this.id
}

output "bucket_url" {
  description = "Bucket URL"
  value       = google_storage_bucket.this.url
}
