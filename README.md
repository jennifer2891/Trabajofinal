# Chatbot Web con Flask y API de IA

Este proyecto implementa un chatbot web utilizando Flask como backend y JavaScript para el frontend. El chatbot puede utilizar tanto la API de Mistral como la de OpenAI para generar respuestas.

## Configuración del entorno de desarrollo

1. Asegúrate de tener Python 3.7 o superior instalado en tu sistema.

2. Crea un entorno virtual:
3. Instala las dependencias: `pip install -r requirements.txt`
4. Configura las variables de entorno:
    export FLASK_APP=app.py
    export AI_API_KEY=tu_api_key  # Reemplaza con tu clave API de Mistral u OpenAI
    export AI_PROVIDER=mistral  # o 'openai' para usar OpenAI

## Ejecución y prueba del proyecto

1. Activa el entorno virtual.
2. Ejecuta la aplicación Flask: `flask run`
3. Abre tu navegador web y visita `http://127.0.0.1:5000/`.
4. Interactúa con el chatbot.
5. Para cambiar entre Mistral y OpenAI, modifica la variable de entorno AI_PROVIDER o actualiza el valor en el archivo config.py.
