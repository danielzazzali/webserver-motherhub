from flask import Flask, render_template
from config.config import load_env, get_env_variable
from controllers.mode_controller import mode_bp
from controllers.network_controller import network_bp, get_devices
from controllers.wifi_controller import wifi_bp, get_ap_info_route

load_env()

port = int(get_env_variable('PORT'))

app = Flask(__name__)
app.register_blueprint(network_bp)
app.register_blueprint(wifi_bp)
app.register_blueprint(mode_bp)
@app.route('/')
def index():
    return render_template('index.html')


def test_api():
    with app.test_client() as client:

        response_devices = client.get('/devices')
        print(response_devices.get_json())

        response_ap = client.get('/ap_info')
        print(response_ap.get_json())

        response_mode = client.get('/mode')
        print(response_mode.get_json())

        new_mode = "AP"
        #response_set_mode = client.post('/mode', json={'mode': new_mode})
        #print(response_set_mode.get_json())

        response_mode = client.get('/mode')
        print(response_mode.get_json())

        #new_ssid = "Kvn"
        #response_change_ssid = client.post(f'/change_ssid/{new_ssid}')
        #print(response_change_ssid.get_json())

        #new_password = "12345678b"
        #response_change_password = client.post(f'/change_password/{new_password}')
        #print(response_change_password.get_json())





if __name__ == '__main__':
    app.run(port=port)