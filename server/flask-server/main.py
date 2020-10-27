from flask import Flask
from flask import request
from flask_httpauth import HTTPBasicAuth
import json
from flask_mqtt import Mqtt
import sys
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
app.config['MQTT_BROKER_URL'] = 'mosquitto'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

# http basic auth credentials
users = {
    "user": "password"
}



@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@app.route('/alert', methods=['POST'])
@auth.login_required
def alert():
#    client.connect("localhost", 1883, 60)
#    data = json.loads(request.data.decode('utf-8'))
#    if data['state'] == 'alerting':
#    client.disconnect()
    return "ok"

@app.route('/control_cmd',methods=['POST','OPTIONS'])
def control_cmd():
    #Send ON Command to MQTT Broker
 
    mqtt.publish("cmd/myfarm/dorm-room/gateway/switch/","on",2)
    return "ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
