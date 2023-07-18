import pika,json


# Setting up the connections
params = pika.URLParameters("amqps://kksedkoa:mY6RFIJ5g4cmhWSaczyd0VWVKrqSROCR@cougar.rmq.cloudamqp.com/kksedkoa")
connection = pika.BlockingConnection(params)

channel = connection.channel()


# function publish that handles the sending of the message. 
# The method parameter is the information about a message
# and body is the message to be sent.

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
    # We also supply a property as contents of the 
    # method and pass it as one of the parameters of 
    # channel.basic_publish. We will use the default 
    # exchange denoted by exchange='' that lets us 
    # specify which queue the message is going.