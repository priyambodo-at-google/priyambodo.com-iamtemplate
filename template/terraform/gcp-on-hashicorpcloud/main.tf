# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

resource "google_compute_instance" "default" {
  name         = var.instance_name
  machine_type = var.machine_type
  zone         = var.gcp_zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "vpc-default-by-doddipriyambodo"
    access_config {
      # Ephemeral IP
    }
  }

  labels = {
    name = var.instance_name
  }
}
