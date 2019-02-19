FROM python:3.7

# Install required packages
ADD setup.py /code/
WORKDIR /code
RUN pip install -e .[dev]

# Add the codebase to the image
ADD . /code
WORKDIR /code
CMD pylint -j 0 dm_management
