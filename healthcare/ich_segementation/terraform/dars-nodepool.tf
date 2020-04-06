# - - - - - - - - - - - 
# dars node pool config
# - - - - - - - - - - -

resource "google_container_node_pool" "dars_node_pool" {
  name       = "spark-pool"
  location   = "${var.location}"
  cluster    = google_container_cluster.kf-hc.name
  node_count = 5
  node_config {
    machine_type = "n1-standard-16"
    disk_size_gb = "1024"
    min_cpu_platform = "${var.min_cpu_platform}"
    oauth_scopes = [
      "https://www.googleapis.com/auth/compute",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
    image_type = "Ubuntu"
    local_ssd_count = 1
    labels = {
      usage = "dev-cluster"
    }
    service_account = "${var.service_account}"
    tags = [
      "healthcare-usecase-dev",
      "dars"
    ]
  }
  management {
    auto_repair = true
  }
  autoscaling {
    min_node_count = 5
    max_node_count = 7
  }
}
