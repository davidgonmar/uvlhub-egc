from flask import render_template
from app.modules.chatbot import chatbot_bp


@chatbot_bp.route('/chatbot', methods=['GET'])
def index():
    return render_template('chatbot/index.html')
