import pika
import sys
import os
from googletrans import Translator

translator = Translator()


LANGUAGES = {
    '1': 'fr',  # French
    '2': 'es',  # Spanish
    '3': 'de',  # German
    '4': 'tr'   # Turkish
}

def main():
    try:
       
        print("Choose a language for translation:")
        print("1. French")
        print("2. Spanish")
        print("3. German")
        print("4. Turkish")
        language_choice = input("Enter the number corresponding to your choice: ")

     
        if language_choice not in LANGUAGES:
            print("Invalid choice. Please select a valid number (1-4).")
            sys.exit(1)

       
        selected_language = LANGUAGES[language_choice]

        print(f"Language selected: {selected_language.upper()}")

        
        print("Connecting to RabbitMQ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        print("Connection established.")

        print("Declaring queue 'translate_queue'...")
        channel.queue_declare(queue='translate_queue')

    except Exception as e:
        print(f"Error setting up RabbitMQ: {e}")
        return

    def callback(ch, method, properties, body):
        try:
           
            original_message = body.decode('utf-8')
            print(f" Received: '{original_message}'")

            
            translated_message = translator.translate(original_message, dest=selected_language).text
            print(f" Translated message: '{translated_message}'")

        except Exception as e:
            print(f"Error during translation: {e}")

   
    channel.basic_consume(queue='translate_queue', on_message_callback=callback, auto_ack=True)
    print("Waiting for messages. To exit, press CTRL+C")
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted by user.")
    except Exception as e:
        print(f"Error in message consumption: {e}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
