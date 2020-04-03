# Helm chart for creating local volumes on Kubernetes

This chart can be used to configure local persistent volumes on Kubernetes given a specific filesystem mount point on each Kubernetes node. This chart assumes the existence of a common mount point on each node to be used as a local persistent volume on Kubernetes.

## How to use
- Modify `values.yaml`, specify the common mount point for the persistent storage on the Kubernetes nodes, then configure the hostnames of the given nodes.
- Run:
```bash
helm install <path-to-this-directory>
```
