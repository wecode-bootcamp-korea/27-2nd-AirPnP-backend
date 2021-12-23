FROM ubuntu:20.04

WORKDIR /usr/src/app

COPY requirements.txt ./requirements.txt

RUN apt-get update \
    && apt-get install python3.9 -y \
    && apt-get install python3-pip -y \
    && apt-get install libmysqlclient-dev -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "airpnp.wsgi:application"] 