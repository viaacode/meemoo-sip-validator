# This dockerfile is used for testing in CI/CD

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    openjdk-17-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY . /workspace
RUN pip3 install ".[dev]" --extra-index-url http://do-prd-mvn-01.do.viaa.be:8081/repository/pypi-all/simple --trusted-host do-prd-mvn-01.do.viaa.be

CMD ["bash"]
