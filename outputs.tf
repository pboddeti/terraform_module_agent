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

output "created_objects" {
  description = "Map of created objects with their metadata"
  value       = {
    for name, obj in google_storage_bucket_object.objects : name => {
      name         = obj.name
      content_type = obj.content_type
      size         = obj.size
      self_link    = obj.self_link
    }
  }
}
