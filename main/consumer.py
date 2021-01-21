#
from main import Product, db
import pika
import json
# from pika import channel

params = pika.URLParameters(
    "amqps://bqtgbmxk:V8vf09KDz2AaBcrd-CNaZ1aC3dVfpp7F@orangutan.rmq.cloudamqp.com/bqtgbmxk")

connection = pika.BlockingConnection(params)

channel = connection.channel()


channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Receive in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(
            id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data['id'])
        db.session.delete(product)
        db.session.commit()


channel.basic_consume(
    queue='main', on_message_callback=callback, auto_ack=True)

print('started consuming')

channel.start_consuming()
channel.close()
