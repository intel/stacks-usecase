resource "google_container_cluster" "kf-hc" {
  name = "kf-hc"
  location = "${var.location}"
  node_version = "${var.node_version}"
  min_master_version = "${var.node_version}"
  network = google_compute_network.ProdNet.self_link
  subnetwork = google_compute_subnetwork.ProdSubnet.self_link
  remove_default_node_pool = true
  initial_node_count = 1

  master_auth {
    password = "${var.master_auth_pass}"
    username = "${var.master_auth_user}"
  }
  resource_labels = {
    application = "kubeflow"
  }
}

# - - - - - - - - - - - -
# kubeflow node pool config
# - - - - - - - - - - - -

resource "google_container_node_pool" "kubeflow_node_pool" {
  name       = "kf-hc-cpu-pool-v1"
  location   = "${var.location}"
  cluster    = google_container_cluster.kf-hc.name
  node_count = 2
  node_config {
    machine_type = "n1-standard-8"
    disk_size_gb = "1024"
    min_cpu_platform = "${var.min_cpu_platform}"
    oauth_scopes = [
      "https://www.googleapis.com/auth/compute",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
    image_type = "COS"
    local_ssd_count = 1
    labels = {
      usage = "dev-cluster"
    }
    service_account = "${var.service_account}"
    tags = [
      "healthcare-usecase-dev"
    ]
  }
  management {
    auto_repair = true
  }
  autoscaling {
    min_node_count = 2
    max_node_count = 10
  }
}
