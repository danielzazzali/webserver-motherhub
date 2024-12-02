from flask import Blueprint, jsonify, request
from models.device_mode_model import get_device_mode, set_device_mode, delayed_reboot, delayed_shutdown

mode_bp = Blueprint('mode', __name__)


@mode_bp.route('/device_mode', methods=['GET'])
def get_device_mode_route():
    try:
        mode = get_device_mode()
        return jsonify({'mode': mode}), 200
    except (EnvironmentError, FileNotFoundError, ValueError) as e:
        return jsonify({'error': str(e)}), 400


@mode_bp.route('/device_mode', methods=['POST'])
def set_device_mode_route():
    try:
        new_mode = request.json.get('mode')
        set_device_mode(new_mode)
        return jsonify({'message': 'Mode set successfully'}), 200
    except (EnvironmentError, FileNotFoundError, ValueError) as e:
        return jsonify({'error': str(e)}), 400


@mode_bp.route('/reboot', methods=['POST'])
def reboot():
    delayed_reboot()
    return jsonify({"message": "System is rebooting"}), 200

@mode_bp.route('/shutdown', methods=['POST'])
def shutdown():
    delayed_shutdown()
    return jsonify({"message": "System is shutting down"}), 200