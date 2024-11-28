# RELK Project README

## Introduction

Welcome to the **RELK** repository! This project demonstrates how to connect the ELK Stack (Elasticsearch, Logstash, Kibana) with RabbitMQ to send data from a producer to a consumer and store it in a PostgreSQL database.

---

## Prerequisites

- **Docker and Docker Compose**: Ensure these are installed on your system.
- **Basic Knowledge**: Familiarity with Docker and the command-line interface is helpful.

---

## Steps

### 1. Create a Flask Project
- Develop a Flask application to handle JSON data.
- Use Postman (or similar tools) to send JSON data. Example data structure:
  ```json
  {
    "username": "example",
    "password": "password123",
    "age": 25,
    "region": "North"
  }
  ```
- To retrieve database entries, send the following request:
  ```json
  {"show": "mytable"}
  ```

### 2. Set Up RabbitMQ
- Create a RabbitMQ container to queue data from the producer and send it to ELK.

### 3. Configure Logstash
- Use Logstash for logging and data pipeline management.
- The repository includes a `logstash.conf` file to pipeline data from the producer and consumer, forwarding it to Elasticsearch.

### 4. Deploy Elasticsearch
- Set up an Elasticsearch container as the search and analytics engine to index, store, and enable querying of data.

### 5. Access Kibana
- Open your browser and navigate to [http://localhost:5601](http://localhost:5601) to visualize and explore the data.

### 6. Develop the Consumer
- Create a consumer to process incoming data from RabbitMQ and query the PostgreSQL database.

### 7. Set Up PostgreSQL
- Use PostgreSQL as the database to store the processed data.

---

## Conclusion

Congratulations! You now have a fully functioning **RELK** stack. Feel free to reach out with any questions or comments—I’m happy to help!
