FROM python:3.10-slim

RUN mkdir /code
WORKDIR /code

# Install required packages
COPY setup.py pyproject.toml poetry.lock /code/
RUN set -e; \
    apt-get update \
    && apt-get install -y --no-install-recommends gcc libc-dev \
    && pip install poetry==1.2.2 \
    && poetry install \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove gcc libc-dev

# Add the codebase to the image
COPY . /code
# Re-run the install to ensure api_boilerplate is installed as a top-level package
RUN poetry install
ENTRYPOINT [ "lib/docker/entrypoint.sh" ]
