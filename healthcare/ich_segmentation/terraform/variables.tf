variable "project" {
	type = string
	default = "YOUR_PROJECT-ACCOUNT-NUMBER"
}

variable "region" {
	type = string
	default = "YOUR_REGION"
}

variable "location" {
	type = string
	default = "YOUR_ZONE"
}


variable "network" {
	type = string
	default = "YOUR_NETWORK_NAME"
}

variable "subnetwork" {
	type = string
	default = "YOUR_SUBNETWORK_NAME"
}

variable "service_account" {
	type = string
	default = "YOUR_SERVICE-ACCOUNT-EMAIL-ADDRESS"
}

variable "credentials_path" {
	type = string
	default = "PATH/TO/YOUR/SERVICE-ACCOUNT.json"
}


variable "min_cpu_platform" {
	type = string
	default = "Intel Skylake"
}


variable "node_version" {
	type = string
	default = "1.14.10-gke.21"
}

variable "master_auth_user" {
	type = string
	default = "YOUR_USERNAME"
}

variable "master_auth_pass" {
	type = string
	default = "YOUR_PASSWORD"
}
