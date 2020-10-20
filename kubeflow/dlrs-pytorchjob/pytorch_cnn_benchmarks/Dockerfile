FROM clearlinux/stacks-pytorch-ubuntu:v0.7.0

WORKDIR /workdir
COPY cnn_benchmarks.py .

ENTRYPOINT ["mpirun", "-n", "1", "--allow-run-as-root", "/bin/python", "/workdir/cnn_benchmarks.py"]
