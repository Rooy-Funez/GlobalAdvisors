
import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Ahora tomamos las claves desde las variables de entorno
TELEGRAM_BOT_API_TOKEN = os.getenv("TELEGRAM_BOT_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Aquí va el ID de tu Assistant personalizado (si lo estás usando)
ASSISTANT_ID = "asst_uqNAF5EqDnjJw1rLqb9GFIhi"  # Reemplaza con el ID de tu Assistant

# Función para llamar a OpenAI con el mensaje del usuario
def consultar_openai(mensaje_usuario):
    openai_url = f"https://api.openai.com/v1/assistants/{ASSISTANT_ID}/completions"

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        "messages": [
            {"role": "user", "content": mensaje_usuario}  # Mensaje del usuario
        ]
    }

    try:
        # Hacer la solicitud a OpenAI usando el Assistant personalizado
        response = requests.post(openai_url, headers=headers, json=data)
        response.raise_for_status()  # Verificar si hubo algún error HTTP
        respuesta = response.json()

        # Verificar si 'choices' está en la respuesta
        if 'choices' in respuesta and len(respuesta['choices']) > 0:
            return respuesta['choices'][0]['message']['content']
        else:
            return "Lo siento, no pude obtener una respuesta válida de OpenAI."

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
        return "Lo siento, hubo un problema con el servidor. Inténtalo de nuevo más tarde."
    except Exception as err:
        print(f"Error: {err}")
        return "Lo siento, hubo un error al procesar tu solicitud."

# Función que se ejecuta cuando el bot recibe un mensaje
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Capturar el mensaje del usuario
    response_text = consultar_openai(user_message)  # Obtener la respuesta desde OpenAI
    update.message.reply_text(response_text)  # Responder al usuario en Telegram

# Inicializar el bot
def main():
    updater = Updater(TELEGRAM_BOT_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Manejar mensajes de texto
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

# Ejecutar el bot
main()
