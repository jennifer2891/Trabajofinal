from flask import Blueprint, render_template, request, jsonify, current_app
from .ai import get_ai_response
from config import Config

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/send', methods=['POST'])
def send():
    user_message = request.json['message']
    ai_provider = Config.AI_PROVIDER
    current_app.logger.info(f"Mensaje recibido: {user_message}")
    current_app.logger.info(f"Proveedor de IA seleccionado: {ai_provider}")
    
    try:
        response_message = get_ai_response(user_message, ai_provider)
        current_app.logger.info(f"Respuesta generada: {response_message}")
        return jsonify({'response': response_message})
    except Exception as e:
        current_app.logger.error(f"Error al generar respuesta: {str(e)}")
        return jsonify({'response': "Lo siento, ocurrió un error al procesar tu solicitud. Por favor, inténtalo de nuevo más tarde."}), 500