from flask import Blueprint, jsonify
from models.network_model import get_connected_devices

network_bp = Blueprint('network', __name__)


@network_bp.route('/devices', methods=['GET'])
def get_devices():
    try:
        devices = get_connected_devices()
        return jsonify(devices), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
