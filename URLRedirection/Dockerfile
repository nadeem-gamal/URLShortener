FROM python:3.10.14-alpine3.20

COPY requirements.txt /app/requirements.txt
COPY templates /app/templates

WORKDIR /app
RUN pip install -r requirements.txt
RUN export FLASK_ENV=development
RUN export FLASK_APP=app.py

COPY app.py /app/app.py

EXPOSE 5000/tcp
# ENTRYPOINT flask run --host=0.0.0.0
ENTRYPOINT gunicorn -b 0.0.0.0:5000 -w 2 app:app
