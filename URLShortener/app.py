from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
import base64
import random
import os
from flask_caching import Cache
import redis
import pika
import threading
import time


app = Flask(__name__)

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'redis'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0

cache = Cache(app=app)
cache.init_app(app)

# redis_client = redis.Redis(host='redis', port=6379, db=0)

db_username = os.environ['URL_POSTGRES_USER']
db_password = os.environ['URL_POSTGRES_PASSWORD']
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_username}:{db_password}@postgres:5432/test_db'
db = SQLAlchemy(app)


# connection = None
# try:
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
# except pika.exceptions.AMQPConnectionError as exc:
#     print("Failed to connect to RabbitMQ service. Message wont be sent.")
#     # return

# channel = connection.channel()
# channel.queue_declare(queue='url_queue', durable=True)

# print(' Waiting for messages...')


# def callback(ch, method, properties, body):
#     print(" Received %s" % body.decode())
#     print(" Done")

#     ch.basic_ack(delivery_tag=method.delivery_tag)

# channel.basic_qos(prefetch_count=1)
# channel.basic_consume(queue='task_queue', on_message_callback=callback)
# channel.start_consuming()

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_url = db.Column(db.String(2000), nullable=False)
    short_code = db.Column(db.String(255), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<URL %r>' % self.id

       
def clean_old_urls(app_context):
    app_context.push()
    while(True):
        print('clean_old_urls')
        try:
            end_date = date.today() - timedelta(days=1)
            print(end_date)
            url_objs = URL.query.filter(URL.date_created<end_date).all()
            print(url_objs)
            if url_objs is not None:
                print(url_objs)
                for url_obj in url_objs:
                    print(url_obj)
                    db.session.delete(url_obj)
                    db.session.commit()
        except Exception as ex:
            print(ex)
        time.sleep(5)

clean_old_urls_thread = threading.Thread(target=clean_old_urls, args=(app.app_context(), ))
clean_old_urls_thread.daemon = True
clean_old_urls_thread.start()


def generate_short_code(size):
    n = []
    for i in range(size):
        n.append(str(random.randrange(0, 9, 1)))
    return ''.join(n)


@app.route('/urlshortner/create/<url>/<int:length>')
def create(url, length):
    # code = base64.b64encode(url.strip().encode()).decode()
    if length > 255:
        return 'Error: can not create short code larger than 255.'
    if len(url) > 2000:
        return 'Error: can not create short code for URL larger than 2000.'
    code = generate_short_code(length)
    new_url = URL(full_url=url, short_code=code)
    try:    
        db.session.add(new_url)
        db.session.commit()
        # print(new_url)
        # print(jsonify({"short_code": code}))
        return {"short_code": code}, 200
    except Exception as ex:
        print(ex)
        return 'Error while creating a new short URL.'


@app.route('/urlshortner/url/<short_code>')
@cache.cached(timeout=60, key_prefix='urls')
def get_url(short_code):
    # cached_response = redis_client.get('urls')
    # if cached_response:
    #     return jsonify(cached_response)
    url_obj = URL.query.filter(URL.short_code==short_code).first()
    if url_obj is not None:
        print(url_obj.full_url)
        # return redirect(url_obj.full_url), 300
        return jsonify({'url': url_obj.full_url.strip()}), 200
    return 'Error: code not found.', 404
       

if __name__ == "__main__":
    app.run(debug=True)
