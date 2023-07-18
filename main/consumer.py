import pika,json
from main import Product,db,app

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



channel.queue_declare(queue='main')


def callback(ch, method,properties, body):
    print("Received from admin in main")
    print("Message body ",body)
    data = json.loads(body)
    print("After loading json, data is :",data)

    if properties.content_type == 'product_created':
        product = Product(id =data['id'],
                        title = data['title'],
                        image = data['image']
                                   )
        db.session.add(product)
        db.session.commit()
        print("created product")
    
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product['image'] = data['image']

        db.session.commit()
        print("created updated")   
    
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print("created deleted")

        




with app.app_context():
        # We also instruct RabbitMQ to allow our callback
    # function to receive messages from the likes queue.
    channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)


    print('Started consuming')
    
    # Tell our channel to start receiving messages.
    channel.start_consuming()
    channel.close()
    


