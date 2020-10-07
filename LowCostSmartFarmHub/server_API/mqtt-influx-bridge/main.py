#Some of the code was adapted from https://github.com/iothon/docker-compose-mqtt-influxdb-grafana/blob/master/02-bridge/main.py

#This script will recieve MQTT data and save it to a influx Database

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

import time

INFLUXDB_ADDRESS = 'influxdb'
INFLUXDB_USER = 'root'
INFLUXDB_PASSWORD = 'root'
INFLUXDB_DATABASE = 'iothon_db'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)

def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        print('Creating database ' + INFLUXDB_DATABASE)
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

def main:

    time.sleep(10)
    print('Connecting to the database ' + INFLUXDB_DATABASE)
    _init_influxdb_database()
    

if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
