import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


DEFAULT_PROJECT_ID = "arctic-rite-403213"


def run(cmd: list[str], cwd: Path, env: Optional[dict[str, str]] = None) -> None:
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, env=env)
    if result.returncode != 0:
        sys.exit(result.returncode)


def has_valid_adc(cwd: Path, env: Optional[dict[str, str]] = None) -> bool:
    result = subprocess.run(
        ["gcloud", "auth", "application-default", "print-access-token"],
        cwd=cwd,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply Terraform config to create a Google Cloud Storage bucket."
    )
    parser.add_argument(
        "--project-id",
        help=(
            "GCP project ID (optional: overrides Terraform default). "
            f"Terraform default is {DEFAULT_PROJECT_ID}."
        ),
    )
    parser.add_argument("--bucket-name", required=True, help="Globally unique bucket name")
    parser.add_argument("--region", default="us-central1", help="GCP region")
    parser.add_argument(
        "--terraform-dir",
        default="terraform",
        help="Path to Terraform configuration directory",
    )
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Pass -auto-approve to terraform apply",
    )
    parser.add_argument(
        "--output-dir",
        default=".terraform-generated",
        help=(
            "Folder (inside terraform dir) to store generated runtime files "
            "(state + TF data)."
        ),
    )
    parser.add_argument(
        "--setup-gcloud",
        action="store_true",
        help=(
            "Run gcloud auth + project setup before Terraform. "
            "This is interactive and opens a browser login flow."
        ),
    )

    args = parser.parse_args()
    tf_dir = Path(args.terraform_dir).resolve()
    output_dir = (tf_dir / args.output_dir).resolve()
    tf_data_dir = output_dir / "data"
    tf_state_file = output_dir / "state" / "terraform.tfstate"

    if not tf_dir.exists():
        print(f"Terraform directory not found: {tf_dir}")
        sys.exit(1)

    tf_data_dir.mkdir(parents=True, exist_ok=True)
    tf_state_file.parent.mkdir(parents=True, exist_ok=True)

    tf_env = os.environ.copy()
    tf_env["TF_DATA_DIR"] = str(tf_data_dir)

    if args.setup_gcloud:
        gcloud_project = args.project_id or DEFAULT_PROJECT_ID
        run(["gcloud", "auth", "login"], cwd=tf_dir, env=tf_env)
        run(["gcloud", "auth", "application-default", "login"], cwd=tf_dir, env=tf_env)
        run(["gcloud", "config", "set", "project", gcloud_project], cwd=tf_dir, env=tf_env)
    elif not has_valid_adc(cwd=tf_dir, env=tf_env):
        print(
            "No valid Google Application Default Credentials found. "
            "Run with --setup-gcloud or run: gcloud auth application-default login"
        )
        sys.exit(1)

    run(
        [
            "terraform",
            "init",
            "-reconfigure",
            f"-backend-config=path={tf_state_file}",
        ],
        cwd=tf_dir,
        env=tf_env,
    )

    apply_cmd = [
        "terraform",
        "apply",
        "-var", f"bucket_name={args.bucket_name}",
        "-var", f"region={args.region}",
    ]

    if args.project_id:
        apply_cmd.extend(["-var", f"project_id={args.project_id}"])

    if args.auto_approve:
        apply_cmd.append("-auto-approve")

    run(apply_cmd, cwd=tf_dir, env=tf_env)


if __name__ == "__main__":
    main()
