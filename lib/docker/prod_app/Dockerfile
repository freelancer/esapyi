FROM python:3.7

# Install required packages
ADD setup.py /code/
WORKDIR /code
RUN pip install -e .

# Add the codebase to the image
ADD . /code
WORKDIR /code
CMD uwsgi --ini uwsgi_prod_app_config.ini
