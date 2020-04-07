MANIFESTS=./manifests

DEFAULT_NAMESPACE=dars-cluster
DEFAULT_DOCKER_IMAGE=clearlinux/stacks-dars-openblas:latest
DEFAULT_CONFIGMAP_SETUP=setup-files-configmap
DEFAULT_CONFIGMAP_ENV=environment-configmap

HDFS_FILES_BASE=hdfs-nn-statefulset.yaml hdfs-dn-statefulset.yaml
HDFS_FILES=$(addprefix $(MANIFESTS)/,$(HDFS_FILES_BASE))

YARN_FILES_BASE=yarn-rm-statefulset.yaml yarn-nm-statefulset.yaml
YARN_FILES=$(addprefix $(MANIFESTS)/,$(YARN_FILES_BASE))

HADOOP_SERVICES_FILES=hdfs-nn-svc.yaml hdfs-dn-svc.yaml
HADOOP_SERVICES=$(addprefix $(MANIFESTS)/,$(HADOOP_SERVICES_FILES))

SPARK_SERVICES_FILES=svc-master.yaml headless-svc.yaml
SPARK_SERVICES=$(addprefix $(MANIFESTS)/,$(SPARK_SERVICES_FILES))

SPARK_STATEFULSETS_FILES=statefulset-master.yaml
SPARK_STATEFULSETS=$(addprefix $(MANIFESTS)/,$(SPARK_STATEFULSETS_FILES))

PERSISTEN_VOLUMES_FILES=hdfs-dn-pvc.yaml
PERSISTEN_VOLUMES=$(addprefix $(MANIFESTS)/,$(PERSISTEN_VOLUMES_FILES))

ifndef NAMESPACE
NAMESPACE := $(DEFAULT_NAMESPACE)
endif

ifndef DOCKER_IMAGE
DOCKER_IMAGE := $(DEFAULT_DOCKER_IMAGE)
endif

all: init create-all-services create-all-apps
init: create-ns create-configmap
stop: delete-all-apps delete-all-services delete-configmap delete-ns
	@while [[ -n `kubectl get ns -o json | jq 'select(.items[].status.phase=="Terminating") | true'` ]]; \
	  do echo "Waiting for $(NAMESPACE) namespace termination" ; sleep 5; done

### S P A R K  O N   Y A R N  ###
### All apps
create-all-apps: hadoop spark
delete-all-apps: hadoop-stop spark-stop

### Services
create-all-services: create-hadoop-services create-spark-services
delete-all-services: delete-hadoop-services delete-spark-services

### S P A R K   ###
spark: init create-spark-services create-spark-apps
spark-stop: delete-spark-apps delete-spark-services
create-spark-apps: create-spark-statefulsets
delete-spark-apps: delete-spark-statefulsets
create-spark-services: $(SPARK_SERVICES)
delete-spark-services: $(addsuffix .delete,$(SPARK_SERVICES)) delete-statefulset-pods-service

### H A D O O P   ###
hadoop: init create-hadoop-services create-hadoop-pvc create-hadoop-apps
hadoop-stop: delete-hadoop-apps delete-hadoop-services delete-hadoop-pvc
# create-hadoop-apps: create-hdfs create-yarn
create-hadoop-apps: create-hdfs
delete-hadoop-apps: delete-yarn delete-hdfs
create-hadoop-services: $(HADOOP_SERVICES)
delete-hadoop-services: $(addsuffix .delete,$(HADOOP_SERVICES)) delete-statefulset-pods-service
create-hadoop-pvc: $(PERSISTEN_VOLUMES)
delete-hadoop-pvc: $(addsuffix .delete,$(PERSISTEN_VOLUMES)) delete-statefulset-pods-service

### C O M M O N  T A R G E T S ###
### Config Map
create-configmap: kubectl
	if [[ `$(KUBECTL) get cm | grep $(DEFAULT_CONFIGMAP_SETUP)` ]]; then \
		echo "config map $(DEFAULT_CONFIGMAP_SETUP) already created"; \
	else \
		$(KUBECTL) create configmap $(DEFAULT_CONFIGMAP_SETUP) \
		--from-file=artifacts/bootstrap.sh \
		--from-file=artifacts/start-yarn-rm.sh \
		--from-file=artifacts/start-yarn-nm.sh \
		--from-file=artifacts/slaves \
		--from-file=artifacts/core-site.xml \
		--from-file=artifacts/hdfs-site.xml \
		--from-file=artifacts/mapred-site.xml \
		--from-file=artifacts/yarn-site.xml \
		--from-file=artifacts/log4j.properties; \
		$(KUBECTL) create -f manifests/$(DEFAULT_CONFIGMAP_ENV).yaml; \
	fi

delete-configmap: kubectl
	-$(KUBECTL) delete configmap $(DEFAULT_CONFIGMAP_SETUP)
	-$(KUBECTL) delete configmap $(DEFAULT_CONFIGMAP_ENV)

get-configmap: kubectl
	$(KUBECTL) get configmap $(DEFAULT_CONFIGMAP_SETUP) -o=yaml
	$(KUBECTL) get configmap $(DEFAULT_CONFIGMAP_ENV) -o=yaml

### Namespace
create-ns:
	if [[ `kubectl get ns | grep $(NAMESPACE)` ]]; then \
		echo "Namespace $(NAMESPACE) already created"; \
	else \
		kubectl --namespace $(NAMESPACE) create namespace $(NAMESPACE); \
		while [[ -z `kubectl get ns $(NAMESPACE) -o json | jq 'select(.status.phase=="Active") | true'` ]]; \
		do echo "Waiting for $(NAMESPACE) namespace creation" ; sleep 5; done; \
	fi

delete-ns: # $(addsuffix .delete,$(NAMESPACE_FILES))
	if [[ `kubectl --namespace $(NAMESPACE) get ns | grep $(NAMESPACE)` ]]; then \
		kubectl --namespace $(NAMESPACE) delete namespace $(NAMESPACE); \
	fi

### Executable dependencies
KUBECTL_BIN := $(shell command -v kubectl 2> /dev/null)
kubectl:
ifndef KUBECTL_BIN
	$(warning install first minikube)
	exit 1
endif
	$(eval KUBECTL := kubectl --namespace $(NAMESPACE))

# Create by file
$(MANIFESTS)/%.yaml: kubectl
	cat $(value @) | sed "s|STACKIMAGE|$(DOCKER_IMAGE)|g" | $(KUBECTL) apply -f -

# Delete by file
$(MANIFESTS)/%.yaml.delete: kubectl
	-$(KUBECTL) delete -f $(@:.delete=)

# Delete pod name
delete-pod-%: kubectl
	$(KUBECTL) delete pod $*

delete-statefulset-pods-%: kubectl
	-@for pod in `$(KUBECTL) get pods -l component=$* -o json | jq -r '.items[].metadata.name'`; do make delete-pod-$$pod; done

get-ns: kubectl
	$(KUBECTL) get ns

get-statefulsets: kubectl
	$(KUBECTL) get statefulsets

get-pods: kubectl
	$(KUBECTL) get pods

get-svc: kubectl
	$(KUBECTL) get services

wait-for-pod-%: kubectl
	@while [[ -z `$(KUBECTL) get pods $* -o json | jq 'select(.status.phase=="Running") | true'` ]]; \
	  do echo "Waiting for $* pod" ; sleep 2; done

logs-%: kubectl
	$(KUBECTL) logs $*

get-pod-%: wait-for-pod-%
	@echo "$*"

shell-%: wait-for-pod-%
	$(KUBECTL) exec -it $* -- bash

delete-%-pf: kubectl
	-pkill -f "kubectl.*port-forward.*$*.*"

### H A D O O P  T A R G E T S ###
create-hdfs: $(HDFS_FILES)
delete-hdfs: $(addsuffix .delete,$(HDFS_FILES)) delete-statefulset-pods-hdfs-dn delete-statefulset-pods-hdfs-nn
scale-dn: kubectl
	@CURR=`$(KUBECTL) get statefulset hdfs-dn -o json | jq -r '.status.replicas'` ; \
	IN="" && until [ -n "$$IN" ]; do read -p "Enter number of HDFS Data Node replicas (current: $$CURR): " IN; done ; \
	$(KUBECTL) patch statefulset hdfs-dn -p '{"spec":{"replicas": '$$IN'}}'

# create-yarn: $(YARN_FILES)
delete-yarn: delete-yarn-rm-pf $(addsuffix .delete,$(YARN_FILES)) delete-statefulset-pods-yarn-nm delete-statefulset-pods-yarn-rm
scale-nm: kubectl
	@CURR=`$(KUBECTL) get statefulset yarn-nm -o json | jq -r '.status.replicas'` ; \
	IN="" && until [ -n "$$IN" ]; do read -p "Enter number of YARN Node Manager replicas (current: $$CURR): " IN; done ; \
	$(KUBECTL) patch statefulset yarn-nm -p '{"spec":{"replicas": '$$IN'}}'

dfsreport: wait-for-pod-hdfs-nn-0
	$(KUBECTL) exec  hdfs-nn-0 -- hdfs dfsadmin -report

get-yarn-nodes: wait-for-pod-yarn-rm-0
	$(KUBECTL) exec  yarn-rm-0 -- yarn node -list

hadoop-pf-rm: wait-for-pod-yarn-rm-0
	$(KUBECTL) port-forward yarn-rm-0 8088:8088 2>/dev/null &

hadoop-pf: hadoop-pf-rm

hadoop-delete-pf: kubectl delete-yarn-rm-pf

# test targets
wait-hadoop: wait-for-pod-yarn-rm-0
	# Wait until Nodes are ready
	@while [[ `$(KUBECTL) exec  yarn-rm-0 -- yarn node -list | grep Nodes | cut -d ':' -f2` -le 0 ]]; do echo "Waiting for Live Nodes"; sleep 10; done
	@while [[ -z `$(KUBECTL) exec  hdfs-nn-0 -- hdfs dfsadmin -report | grep Name | cut -d ':' -f2` ]]; do echo "Waiting for Datanodes"; sleep 10; done

hadoop-test: wait-hadoop
	$(eval HADOOP_VERSION := $(shell $(KUBECTL) exec  yarn-nm-0 hadoop version | grep Hadoop | cut -d ' ' -f2 ))
	$(KUBECTL) exec  yarn-nm-0 -- hadoop jar /usr/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-$(HADOOP_VERSION)-tests.jar \
	  TestDFSIO -write -nrFiles 5 -fileSize 128MB -resFile /tmp/TestDFSIOwrite.txt

### S P A R K  T A R G E T S ###
### Statefulsets
create-spark-statefulsets: $(SPARK_STATEFULSETS)
delete-spark-statefulsets: $(addsuffix .delete,$(SPARK_STATEFULSETS)) delete-statefulset-pods-statefulset
scale-worker: kubectl
	@CURR=`$(KUBECTL) get statefulset spark-dars-worker -o json | jq -r '.status.replicas'` ; \
	IN="" && until [ -n "$$IN" ]; do read -p "Enter number of Spark workers replicas (current: $$CURR): " IN; done ; \
	$(KUBECTL) patch statefulset spark-dars-worker -p '{"spec":{"replicas": '$$IN'}}'

spark-pf: spark-pf-rm

spark-delete-pf: kubectl delete-spark-dars-master-0-pf

submit-job-on-yarn:
        $(KUBECTL) -n $NAMESPACE cp ../main.py  spark-dars-master-0:/root/main.py
	$(KUBECTL) -N $NAMESPACE exec spark-dars-master-0 -- bash -c "spark-submit --master yarn --deploy-mode cluster /root/main.py"
