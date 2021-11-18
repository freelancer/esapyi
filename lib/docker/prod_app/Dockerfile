FROM python:3.10-slim

# Install required packages
ADD setup.py /code/
WORKDIR /code
RUN set -e; \
    apt-get update \
    && apt-get install -y --no-install-recommends gcc libc-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -e . \
    && apt-get purge -y --auto-remove gcc libc-dev

# Add the codebase to the image
ADD . /code
WORKDIR /code
CMD uwsgi --ini uwsgi_prod_app_config.ini
