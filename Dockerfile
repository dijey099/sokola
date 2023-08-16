FROM python:3.10-alpine

ADD ./static/. /sokola_app/static
COPY ./admin.html /sokola_app
COPY ./index.html /sokola_app
COPY ./requirements.txt /sokola_app
COPY ./server.py /sokola_app

WORKDIR /sokola_app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "server.py"]
