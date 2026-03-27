# Terraform GCS Bucket (Basic)

Basic project structure to create a Google Cloud Storage bucket using Terraform, with a small Python entry script.

## Structure

- `main.py` — runs `terraform init` and `terraform apply`
- `terraform/main.tf` — provider + bucket resource
- `terraform/variables.tf` — input variables

## Prerequisites

- Terraform installed
- Python 3.9+
- Google Cloud authentication configured (for example using ADC):
  - `gcloud auth application-default login`

## Usage

```bash
python main.py \
  --bucket-name YOUR_UNIQUE_BUCKET_NAME \
  --auto-approve
```

Defaults already set:
- `project_id`: `arctic-rite-403213` (in `terraform/variables.tf`)
- `region`: `us-central1`

Optional override:

```bash
python main.py \
  --project-id YOUR_GCP_PROJECT_ID \
  --region us-central1 \
  --bucket-name YOUR_UNIQUE_BUCKET_NAME \
  --auto-approve
```

If you want the script to run `gcloud` auth + project setup first (interactive login), use:

```bash
python main.py \
  --bucket-name YOUR_UNIQUE_BUCKET_NAME \
  --setup-gcloud \
  --auto-approve
```

## Generated files

When you run `main.py`, Terraform runtime files are grouped under:

- `terraform/.terraform-generated/`
  - `data/` (Terraform working/plugin data via `TF_DATA_DIR`)
  - `state/terraform.tfstate` (local state file via Terraform local backend)

You can change this folder with:

```bash
python main.py \
  --bucket-name YOUR_UNIQUE_BUCKET_NAME \
  --output-dir .tf-run \
  --auto-approve
```

Note: `terraform/.terraform.lock.hcl` is still created in the Terraform config folder by Terraform.

## Notes

- Bucket names must be globally unique.
- This is intentionally minimal for a starter setup.
