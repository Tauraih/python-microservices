#
import pika
import json
# from pika import channel

params = pika.URLParameters(
    "amqps://bqtgbmxk:V8vf09KDz2AaBcrd-CNaZ1aC3dVfpp7F@orangutan.rmq.cloudamqp.com/bqtgbmxk")

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main',
                          body=json.dumps(body), properties=properties)
