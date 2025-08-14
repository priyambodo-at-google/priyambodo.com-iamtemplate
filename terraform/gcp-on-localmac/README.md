# Terraform Cloud Getting Started Guide Example (Google Cloud)

This is an example Terraform configuration intended for use with the [Terraform Cloud Getting Started Guide](https://learn.hashicorp.com/terraform/cloud-gettingstarted/tfc_overview), adapted for Google Cloud.

## What will this do?

This is a Terraform configuration that will create a Compute Engine instance in your Google Cloud project.

When you set up a Workspace on Terraform Cloud, you can link to this repository. Terraform Cloud can then run `terraform plan` and `terraform apply` automatically when changes are pushed. For more information on how Terraform Cloud interacts with Version Control Systems, see [our VCS documentation](https://www.terraform.io/docs/cloud/run/ui.html).

## What are the prerequisites?

You must have a Google Cloud account and provide your GCP credentials to Terraform Cloud. Terraform Cloud encrypts and stores variables using [Vault](https://www.vaultproject.io/). For more information on how to store variables in Terraform Cloud, see [our variable documentation](https://www.terraform.io/docs/cloud/workspaces/variables.html).

You will need to set the `gcp_project` variable. You may also need to provide credentials via environment variables.
