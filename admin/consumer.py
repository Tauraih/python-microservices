import json
import pika
from products.models import Product
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()


# from pika import channel

params = pika.URLParameters(
    "amqps://bqtgbmxk:V8vf09KDz2AaBcrd-CNaZ1aC3dVfpp7F@orangutan.rmq.cloudamqp.com/bqtgbmxk")

connection = pika.BlockingConnection(params)

channel = connection.channel()


channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Receive in admin')
    data = json.loads(body)
    print(data)
    product = Product.objects.get(id=data)
    product.ikes = product.likes + 1
    product.save()
    print('product likes increased')


channel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)

print('started consuming')

channel.start_consuming()
channel.close()
