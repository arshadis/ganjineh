from confluent_kafka import Consumer, KafkaError

# Kafka Consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker
    'group.id': 'my-consumer-group',        # Consumer group ID
    'auto.offset.reset': 'earliest'         # Start reading at the earliest message
}

# Create Consumer instance
consumer = Consumer(conf)

# Subscribe to a topic
consumer.subscribe(['my-first-topic'])

# Poll for new messages
try:
    while True:
        msg = consumer.poll(1.0)  # Wait for a message for 1 second
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print(f"Reached end of partition {msg.partition()} at offset {msg.offset()}")
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            # Message is properly received
            print(f"Received message: {msg.value().decode('utf-8')} from {msg.topic()} [{msg.partition()}]")

except KeyboardInterrupt:
    pass

finally:
    # Close down consumer cleanly
    consumer.close()
