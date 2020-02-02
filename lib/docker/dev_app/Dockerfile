FROM python:3.8

# Install required packages
ADD setup.py /code/
WORKDIR /code
RUN pip install -e .[dev]

# Add the codebase to the image
ADD . /code
WORKDIR /code
CMD python api_boilerplate/app.py
