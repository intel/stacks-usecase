FROM clearlinux/stacks-pytorch-mkl:v0.4.0

WORKDIR /efficient_net/
COPY . /efficient_net/
RUN /opt/conda/bin/pip install -r requirements.txt
RUN echo -e "\e[31mThis server should only be used for debugging purposes."
ENTRYPOINT ["/opt/conda/bin/python", "-c ", "hypercorn","-kuvloop", "-b0.0.0.0:5059", "--debug", "-w8"]
CMD ["rest:app"]
