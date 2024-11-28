from flask import Blueprint, jsonify, request
from models.mode_model import get_mode, set_mode

mode_bp = Blueprint('mode', __name__)

@mode_bp.route('/mode', methods=['GET'])
def get_mode_route():
    try:
        mode = get_mode()
        return jsonify({'mode': mode}), 200
    except (EnvironmentError, FileNotFoundError, ValueError) as e:
        return jsonify({'error': str(e)}), 400


@mode_bp.route('/mode', methods=['POST'])
def set_mode_route():
    try:
        new_mode = request.json.get('mode')
        set_mode(new_mode)
        return jsonify({'message': 'Mode set successfully'}), 200
    except (EnvironmentError, FileNotFoundError, ValueError) as e:
        return jsonify({'error': str(e)}), 400