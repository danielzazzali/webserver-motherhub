from flask import Blueprint, jsonify, request
from models.wifi_model import get_ap_info, change_ssid, change_password

wifi_bp = Blueprint('wifi', __name__)

@wifi_bp.route('/ap_info', methods=['GET'])
def get_ap_info_route():
    try:
        ap_info = get_ap_info()
        return jsonify(ap_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wifi_bp.route('/change_ssid/<new_ssid>', methods=['POST'])
def change_ssid_route(new_ssid):
    success = change_ssid(new_ssid)
    if success:
        return jsonify({"message": "SSID changed successfully"}), 200
    else:
        return jsonify({"error": "Failed to change SSID"}), 500


@wifi_bp.route('/change_password/<new_password>', methods=['POST'])
def change_password_route(new_password):
    success = change_password(new_password)
    if success:
        return jsonify({"message": "Password changed successfully"}), 200
    else:
        return jsonify({"error": "Failed to change password"}), 500