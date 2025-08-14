# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

variable "gcp_project" {
  description = "Google Cloud project ID"
  default     = "work-mylab-machinelearning"
}

variable "gcp_region" {
  description = "Google Cloud region"
  default     = "us-central1"
}

variable "gcp_zone" {
  description = "Google Cloud zone"
  default     = "us-central1-a"
}

variable "machine_type" {
  description = "Type of VM to provision"
  default     = "e2-micro"
}

variable "instance_name" {
  description = "VM instance name"
  default     = "provisioned-by-terraform"
}
