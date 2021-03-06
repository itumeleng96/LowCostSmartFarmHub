#Some of the code was created from https://github.com/iothon/docker-compose-mqtt-influxdb-grafana/blob/master/02-bridge/main.py

#This script will recieve MQTT data and save it to a influx Database

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json
import time

INFLUXDB_ADDRESS = 'influxdb'
INFLUXDB_USER = 'root'
INFLUXDB_PASSWORD = 'root'
INFLUXDB_DATABASE = 'smartFarmHub'

MQTT_TOPIC = "data/#" 
MQTT_ADDRESS = "mosquitto"
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS,8086,INFLUXDB_USER,INFLUXDB_PASSWORD,None)

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC,2)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    
def _send_sensor_data_to_influxdb(sensor_data):
    sensor_data['data']['value']=float(sensor_data['data']['value'])
    print("Sensor Data:",sensor_data)
    print("Sensor Data:",sensor_data['data']['value'])
    json_body=[
        {
            'measurement':sensor_data['sensor_name'],
            'tags':{
                'sensor-connection':sensor_data['sensor_connection']
            },
            'fields':{
                'value':sensor_data['data']['value']
            }

        }
    ]
    influxdb_client.write_points(json_body)

def _send_battery_data_to_influxdb(battery_data):
    battery_data['data']['value']=float(battery_data['data']['value'])
    print("Sensor Data:",battery_data)
    print("Sensor Data:",battery_data['data']['value'])
    json_body=[
        {
            'measurement':battery_data['node_name'],
            'tags':{
                'battery-type':battery_data['battery_type']
            },
            'fields':{
                'value':battery_data['data']['value']
            }
        }
    ]
    influxdb_client.write_points(json_body)
def _send_device_list_to_influxdb(device_data):
    device_data['data']['value']=float(device_data['data']['value'])
    
    json_body=[
        {
            'measurement':device_data['device_name'],
            'tags':{
                'device-connection':'devices'
            },
            'fields':{
                'value':device_data['data']['value']
            }
        }
    ]
    influxdb_client.write_points(json_body)


def _parse_mqtt_message(topic,payload):
    #Decode JSON data
    #check what  published message 
    decoded_payload=json.loads(payload)
    if(topic=='data/myfarm/dorm-room/devices/'):
      _send_device_list_to_influxdb(decoded_payload)
    elif (topic=='data/myfarm/dorm-room/power/'):
      _send_battery_data_to_influxdb(decoded_payload)
    else:
      _send_sensor_data_to_influxdb(decoded_payload)
def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        print('Creating database ' + INFLUXDB_DATABASE)
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

def main():
    time.sleep(10)
    print('Connecting to the database ' + INFLUXDB_DATABASE)
    _init_influxdb_database()

    mqtt_client=mqtt.Client()
    mqtt_client.on_connect= on_connect
    mqtt_client.on_message= on_message

    mqtt_client.connect(MQTT_ADDRESS,1883,60)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
