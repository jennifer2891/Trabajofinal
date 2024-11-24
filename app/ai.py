import requests
import openai
from flask import current_app
from config import Config
import time

def get_mistral_response(user_message, max_retries=3, backoff_factor=2):
    MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
    MISTRAL_API_KEY = Config.MISTRAL_API_KEY

    headers = {
        'Authorization': f'Bearer {MISTRAL_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "messages": [{"role": "user", "content": user_message}],
        "model": "mistral-large-2411"
    }
    
    for attempt in range(max_retries):
        try:
            current_app.logger.info(f"Intento {attempt + 1} de enviar solicitud a Mistral API")
            response = requests.post(MISTRAL_API_URL, headers=headers, json=data, timeout=30)
            current_app.logger.info(f"Respuesta de Mistral API: Status Code {response.status_code}")
            response.raise_for_status()
            content = response.json()
            current_app.logger.info(f"Contenido de la respuesta: {content}")
            return content['choices'][0]['message']['content']
        except requests.exceptions.Timeout:
            current_app.logger.warning(f"Tiempo de espera agotado en el intento {attempt + 1}")
            if attempt < max_retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                current_app.logger.info(f"Esperando {sleep_time} segundos antes de reintentar")
                time.sleep(sleep_time)
            else:
                raise
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error al obtener respuesta de Mistral: {e}")
            if attempt < max_retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                current_app.logger.info(f"Esperando {sleep_time} segundos antes de reintentar")
                time.sleep(sleep_time)
            else:
                return f"Lo siento, no pude obtener una respuesta en este momento después de {max_retries} intentos. Por favor, inténtalo de nuevo más tarde."

def get_openai_response(user_message):
    openai.api_key = Config.OPENAI_API_KEY
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        current_app.logger.error(f"Error al obtener respuesta de OpenAI: {e}")
        return "Lo siento, no pude obtener una respuesta en este momento. Por favor, inténtalo de nuevo más tarde."

def get_ai_response(user_message, ai_provider=None):
    if ai_provider is None:
        ai_provider = Config.AI_PROVIDER
    
    if ai_provider == 'openai':
        return get_openai_response(user_message)
    else:
        return get_mistral_response(user_message)