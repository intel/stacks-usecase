FROM clearlinux/stacks-dlrs-oss:v0.5.1
RUN pip install fdk
WORKDIR workspace
RUN git clone https://github.com/intel/stacks-usecase.git
COPY func.py .
RUN cp stacks-usecase/pix2pix/infer.py . && cp -a stacks-usecase/pix2pix/scripts . && rm -rf stacks-usecase
COPY requirements.txt .
COPY generator_model.h5 models/
RUN pip install -r requirements.txt
RUN touch __init__.py scripts/__init__.py
ENV PYTHONPATH=$PYTHONPATH:/workspace/:/workspace/scripts/
ENTRYPOINT ["fdk", "func.py", "handler"]
