from elasticsearch import Elasticsearch
import time
import json
import time
import os
import psycopg2
import traceback
import re
import pika

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

#Retrieve the database URL from environment variable
DATABASE_URL = os.getenv('DATABASE_URL', SQLALCHEMY_DATABASE_URI)

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def is_user_exist(username,cursor):

    try:
        result ="SELECT username FROM mytable WHERE username = \'"
        result =result +username
        result = result +"\';"
        cursor.execute(result)
    except:
        print("Error")
    str1=str(cursor.fetchone())

    if (str1!='None'):
        return True
    return False

def add_user(body):
    body=body.replace("'",'"')
    data = json.loads(body)
    if (data.get('show')=="mytable"):
        return SELECTstar()
    try:
        
        username = data.get('username')
        password = data.get('password')
        region = data.get('region')
        age = data.get('age')
        if username==None or username=="":
            return({'status': 'Username field is null!'}), 406

        if(password==None):
            return({'status': 'Password field is null!'}), 406
        

        if(region==None):
            return({'status': 'Region field is null!'}), 406     

        if(age==None):
           return({'status': 'Age field is null!'}), 406

        if (len(password) < 8):
            return({'status': 'Password length should be greater than 7.'}), 400
            

        if (not re.search(r".*[a-z].*", password)):
            return({'status': "Password should have character from a to z."}),400
            

        if (not re.search(".*[^a-z,^A-z,^0-9].*", password) ):
            return({'status': "Password should have character other than (A-Z,a-z,0-9)."}),400
            

        conn = get_db_connection()
        cursor = conn.cursor()
       
        if is_user_exist(username,cursor) is True:
            return({'status': 'Username already exist!'}), 403, data
            

        cursor.execute('INSERT INTO mytable (username, password, region, age) VALUES (%s, %s, %s, %s);',
                    (username, password, region, age))
        conn.commit()
        cursor.close()
        conn.close()

        return({'status': 'User added successfully'}), 201
    except :
        traceback.print_exc()
        return({'status':traceback.format_exc()}), 412


def SELECTstar():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mytable;')
    str2=""
    while(True):

        str1=str(cursor.fetchone())
        if(str1=="None"):
            break
        str2+=str1

    conn.commit()
    cursor.close()
    conn.close()

    return(str2)

def dbSide(jsol):

    data=jsol.get("message")
    message =add_user(str(data))
    # message = {
        # 'is_create': True,
        # 'username': 
    # }
    message=str(message)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='result', durable=True)

    channel.basic_publish(exchange='',
                        routing_key='result',
                        body=(message))
    print("result send!:" ,message)
    connection.close()

    return

# es = Elasticsearch("http://localhost:9200")  # Use the service name
time.sleep(30)
es = Elasticsearch(os.environ.get('ELASTICSEARCH_URL'))
print(es)
index_name = "request"  # Replace with your actual index name
jsol=""
while True:
    # Query to fetch the latest data
    query = {
        "query": {
            "match_all": {}
        }
    }
    print(jsol)
    temp=jsol

    response = es.search(index=index_name ,body=query)

    for hit in response['hits']['hits']:
        jsol=(hit['_source'])
        break

    if (jsol!=temp):
        print(jsol)
        dbSide(jsol)

    time.sleep(10)  # Delay before the next fetch

