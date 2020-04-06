FROM clearlinux/stacks-dlrs_2-mkl

RUN swupd clean && swupd bundle-add vim

RUN pip install \
    matplotlib seaborn \
    pillow sklearn nibabel \
    google-cloud-storage \
    cassandra-driver pandas
     
COPY models models
COPY utils utils
COPY local local
COPY *.py ./
COPY *.csv ./
COPY <your-GCP-credentials-file>.json ./

ENV GOOGLE_APPLICATION_CREDENTIALS="/workspace/<your-GCP-credentials-file>.json"
