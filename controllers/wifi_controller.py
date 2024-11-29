from flask import Blueprint, jsonify
from models.wifi_model import get_ap_ssid_and_password, change_ap_ssid, change_ap_password, get_ap_connected_devices

wifi_bp = Blueprint('wifi', __name__)


@wifi_bp.route('/connected_devices', methods=['GET'])
def get_ap_connected_devices_route():
    try:
        devices = get_ap_connected_devices()
        return jsonify(devices), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wifi_bp.route('/ap_ssid_and_password', methods=['GET'])
def get_ap_ssid_and_password_route():
    try:
        ap_info = get_ap_ssid_and_password()
        return jsonify(ap_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wifi_bp.route('/change_ap_ssid/<new_ssid>', methods=['POST'])
def change_ap_ssid_route(new_ssid):
    success = change_ap_ssid(new_ssid)
    if success:
        return jsonify({"message": "SSID changed successfully"}), 200
    else:
        return jsonify({"error": "Failed to change SSID"}), 500


@wifi_bp.route('/change_ap_password/<new_password>', methods=['POST'])
def change_ap_password_route(new_password):
    success = change_ap_password(new_password)
    if success:
        return jsonify({"message": "Password changed successfully"}), 200
    else:
        return jsonify({"error": "Failed to change password"}), 500

