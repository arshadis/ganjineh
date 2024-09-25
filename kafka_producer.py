from confluent_kafka import Producer

# Kafka Producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092'  # Kafka broker
}

# Create Producer instance
producer = Producer(conf)

# Delivery report callback
def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Produce some messages 
for i in range(10):
    producer.produce('my-first-topic', key=str(i), value=f'Message {i}', callback=delivery_report)
    # Wait up to 1 second for events. Callbacks will be triggered by poll()
    producer.poll(1)

# Wait for any outstanding messages to be delivered and delivery report callbacks to be triggered
producer.flush()
