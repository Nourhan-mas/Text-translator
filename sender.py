import pika

message = input("Enter the message you want to send for translation: ")
try:
    print(" Connecting to RabbitMQ...")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    print("Connection established.")
except Exception as e:
    print(f" Error connecting to RabbitMQ: {e}")
    sys.exit(1)

try:
    print(" Declaring queue 'translate_queue'...")
    channel.queue_declare(queue='translate_queue')
except Exception as e:
    print(f"Error declaring queue: {e}")
    connection.close()
    sys.exit(1)

try:
    print(f" Publishing message '{message}' to 'translate_queue'...")
    channel.basic_publish(exchange='', routing_key='translate_queue', body=message)
    print(f" Sent '{message}' for translation")
except Exception as e:
    print(f" Error publishing message: {e}")
finally:
    connection.close()
    print(" Connection closed.")
