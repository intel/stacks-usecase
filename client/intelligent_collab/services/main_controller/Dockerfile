FROM python:3.8-slim-buster

WORKDIR /workspace
COPY . /workspace

RUN pip install --no-cache-dir -U poetry && \
    poetry install

ENTRYPOINT [ "poetry", "run", "python3", "api.py" ]