from flask import Flask, request, redirect, url_for, render_template, jsonify
import requests
import pika


app = Flask(__name__)

# connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
# channel = connection.channel()
# channel.exchange_declare(exchange='widgetexchange', exchange_type='url')


@app.route('/urlshortner/redirect/<short_code>')
def redirect(short_code):
    # try:
    #     connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    # except pika.exceptions.AMQPConnectionError as exc:
    #     print("Failed to connect to RabbitMQ service. Message wont be sent.")
    #     return

    # channel = connection.channel()
    # channel.queue_declare(queue='url_queue', durable=True)
    # channel.basic_publish(
    #     exchange='',
    #     routing_key='url_queue',
    #     body=short_code,
    #     properties=pika.BasicProperties(
    #         delivery_mode=2,  # make message persistent
    #     ))
   
    # connection.close()
    url_obj = requests.get(f'http://url-shortener:5000/urlshortner/url/{short_code}').json()
    if url_obj is not None:
        return jsonify(url_obj)
    return 'Error: code not found.'


if __name__ == "__main__":
    app.run(debug=True)
