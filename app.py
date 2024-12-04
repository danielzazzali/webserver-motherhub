from flask import Flask, render_template


from config.constants import PORT
from controllers.device_mode_controller import mode_bp
from controllers.wifi_controller import wifi_bp


port = int(PORT)
app = Flask(__name__)
app.register_blueprint(mode_bp)
app.register_blueprint(wifi_bp)

@app.route('/')
def index():
    return render_template('index.html')

def test_api():
    with app.test_client() as client:

        #############################################################################
        ###################### Test the mode API  ###################################
        #############################################################################
        # Test the device mode API
        device_mode = client.get('/device_mode')
        print(device_mode.get_json())

        device_mode = client.post('/device_mode', json={'mode': 'NOTAPNORSTA'})
        print(device_mode.get_json())

        #device_mode = client.post('/device_mode', json={'mode': 'AP'})
        #print(device_mode.get_json())

        #############################################################################
        ###################### Test the ethernet API  ###############################
        #############################################################################

        devices = client.get('/connected_devices')
        print(devices.get_json())


        #############################################################################
        ###################### Test the wi-fi API  ##################################
        #############################################################################




if __name__ == '__main__':
    #test_api()
    app.run(port=port)
