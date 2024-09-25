import pika

# Set up the connection parameters to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Create a queue named 'hello' (should be the same as producer)
channel.queue_declare(queue='hello')

# Callback function to process received messages
def callback(ch, method, properties, body):
    print(f" [x] Received :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::{body}")

# Subscribe the consumer to the queue
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C:::::::::::::::::::::::::::::::::::::::::::::::')

# Start consuming messages
channel.start_consuming()
