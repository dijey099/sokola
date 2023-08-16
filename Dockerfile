FROM python:3.4-alpine

ADD . /sokola_app
WORKDIR /sokola_app
RUN pip install -r requirements.txt

CMD ["gunicorn", "server:app", "-b", "0.0.0.0:80"]
