# - - - - - - - - - - - - - - - -
# cassandra prod node pool config
# - - - - - - - - - - - - - - - -

resource "google_container_node_pool" "cassandra_prod_node_pool" {
  name       = "cassandra-prod-pool"
  location   = "${var.location}"
  cluster    = google_container_cluster.kf-hc.name
  node_count = 8
  node_config {
    machine_type = "n1-standard-1"
    disk_size_gb = "1024"
    disk_type = "pd-standard"
    guest_accelerator = []
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
      "cassandra"
    ]
  }
  management {
    auto_repair = true
  }
}
