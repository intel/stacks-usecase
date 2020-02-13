FROM clearlinux/stacks-pytorch-mkl:v0.5.0

WORKDIR /workdir
COPY cnn_benchmarks.py .

ENTRYPOINT ["mpirun", "-n", "1", "--allow-run-as-root", "/opt/conda/bin/python", "/workdir/cnn_benchmarks.py"]
