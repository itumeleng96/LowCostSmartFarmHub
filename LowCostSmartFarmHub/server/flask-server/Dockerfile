FROM python:3.7-alpine

LABEL maintainer="Joseph" \
      description="Flask Server for handling grafana request on PORT:5000"

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "-u", "main.py"]
