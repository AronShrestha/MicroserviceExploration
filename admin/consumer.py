import pika, json, os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product
# Now that we can publish messages, we now create a 
# consumer at our Likes project. Create a consumer.py 
# file in Likes directory. The file should be in the 
# same structure level as manage.py.

# Setting up the connections
params = pika.URLParameters('amqps://kksedkoa:mY6RFIJ5g4cmhWSaczyd0VWVKrqSROCR@cougar.rmq.cloudamqp.com/kksedkoa')
connection = pika.BlockingConnection(params)

channel = connection.channel()


#     We also need to declare a queue that will be receiving 
# the messages. It should be the same name as the one 
# declared in the routing_key parameter in the 
# channels.basic_publish function in producer.py 
# file in the Quotes project.

#     We create a function callback that will be called 
# whenever a message is received. The ch is the channel where 
# communication occurs. method is the information concerning 
# message delivery. properties are user-defined properties on
# the message. body is the message received.



channel.queue_declare(queue='admin')

print("hello from admin consumer")
def callback(ch, method, properties, body):
    print("hello from  inside callback of admin consumer")
    print("Received in admin with ")
    print("json body is",json.loads(body))
    print(body)
    id = json.loads(body)#since we are passing id as a body
    print("got id as ",id)
    product = Product.objects.get(id = id)
    product.likes += 1
    product.save()
    print(f"Product with id:{id} is liked ")





# We also instruct RabbitMQ to allow our callback
# function to receive messages from the likes queue.
channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)


print('Started consuming')
# Tell our channel to start receiving messages.
channel.start_consuming()
channel.close()