FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y build-essential unzip wget python-dev

# Clean apt-get
RUN apt-get clean -y

# Install poetry
RUN pip install "poetry==1.2.1"

# Copy project
COPY . /home/runner/app
WORKDIR /home/runner/app

# Install python requirements
RUN poetry export --format requirements.txt --output requirements.txt --without-hashes
RUN pip install -r requirements.txt

RUN groupadd --gid 1000 runner \
    && useradd --uid 1000 --gid runner --shell /bin/bash --create-home runner

USER runner

CMD [ "python", "-m", "src.main" ]
