FROM python:3.10-alpine

ADD . /sokola_app
WORKDIR /sokola_app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "server.py"]
