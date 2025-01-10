from flask import request, jsonify
from config import Config

def verificar_admin():
    token = request.headers.get('Authorization')
    if token != f"Bearer {Config.ADMIN_TOKEN}":
        return jsonify({"error": "Acesso não autorizado"}), 403
