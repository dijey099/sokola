FROM python:3.4-alpine

ADD . /sokola_app
WORKDIR /sokola_app
RUN pip install -r requirements.txt

CMD ["python", "server.py"]
