import pika

# Set up the connection parameters to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Create a queue named 'hello'
channel.queue_declare(queue='hello')

# Publish a message to the queue
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!::::::::::::::::::::::::::::::::::::::::::::::::::::::::'")

# Close the connection
connection.close()
