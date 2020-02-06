# TensorFlow Training (TFJob) with Kubeflow and DLRS

A [TFJob](https://www.kubeflow.org/docs/components/tftraining) is Kubeflow's custom resource used to run TensorFlow training jobs on Kubernetes.

## Submitting TFJobs


In this folder you will find several TFJob examples that use the Deep Learning Reference Stack as base image for creating the container(s) that will run training workloads in your Kubernetes cluster.
Select one form the list below:

* [Training Tensorflow CNN Benchmarks with DLRS + Intel® MKL-DNN and AVX512-DL Boost](https://github.intel.com/verticals/usecases/tree/master/kubeflow/dlrs-tfjob/tf_cnn_benchmarks)


## Customizing the TFJob

A TFJob is a resource with a YAML representation like the one below. Edit to use the DLRS image containing the code to be executed and modify the command for your own training code.
If you'd like to modify the number and type of replicas, resources, persistent volumes and environment variables, please refer to the Kubeflow documentation:
> Source: [What is a TFJob?](https://www.kubeflow.org/docs/components/tftraining/#what-is-tfjob)

```bash
apiVersion: kubeflow.org/v1
kind: TFJob
metadata:
  generateName: tfjob
  namespace: kubeflow
spec:
  tfReplicaSpecs:
    PS:
      replicas: 1
      restartPolicy: OnFailure
      template:
        spec:
          containers:
          - name: tensorflow
            image: dlrs-image
            command:
              - python
              - -m
              - trainer.task
              - --batch_size=32
              - --training_steps=1000
    Worker:
      replicas: 3
      restartPolicy: OnFailure
      template:
        spec:
          containers:
          - name: tensorflow
            image: dlrs-image
            command:
              - python
              - -m
              - trainer.task
              - --batch_size=32
              - --training_steps=1000
    Master:
          replicas: 1
          restartPolicy: OnFailure
          template:
            spec:
              containers:
              - name: tensorflow
                image: dlrs-image
                command:
                  - python
                  - -m
                  - trainer.task
                  - --batch_size=32
                  - --training_steps=1000
```

For further information, please refer to:
* [Distributed TensorFlow](https://www.tensorflow.org/deploy/distributed).
* [TFJobs](https://www.kubeflow.org/docs/components/tftraining/)
