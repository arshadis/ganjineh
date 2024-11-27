from flask import Flask, jsonify, request
import pika
import os

app = Flask(__name__)

@app.route('/ping')
def ping():
    return {'msg': 'pong!'}
def publish_message_to_rabbitmq(message):
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Declare a queue (make sure the queue exists)
    channel.queue_declare(queue='flask_queue', durable=True)
    # for i in range(5):

    # Publish a message
    channel.basic_publish(exchange='',
                        routing_key='flask_queue',
                        body=(message))
    print("request added!")
    connection.close()

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    # message = data.get('message', 'Default message')

    # Call the function to publish the message to RabbitMQ
    publish_message_to_rabbitmq(str(data))

    return jsonify({'status': 'Message sent to Producer'})

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)

