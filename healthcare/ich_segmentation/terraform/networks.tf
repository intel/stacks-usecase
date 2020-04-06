resource "google_compute_subnetwork" "ProdSubnet" {
  name          = "${var.subnetwork}"
  ip_cidr_range = "192.168.10.0/24"
  region        = "${var.region}"
  network       = google_compute_network.ProdNet.self_link
}

resource "google_compute_network" "ProdNet" {
  name                    = "${var.network}"
  auto_create_subnetworks = false
}
