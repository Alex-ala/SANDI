from flask import Flask
from flask import abort
from flask import request
from paho.mqtt import client as mqtt
from yaml import load
import logging
import logging.handlers
import os

app = Flask(__name__)
base = os.path.dirname(os.path.realpath(__file__))
config = dir()
topics = dir()
#Read config file
def reload_config():
    with open(base + "/config.yml", 'r') as file:
        try:
            global config
            config = (load(file))
            global topics
            topics = config["topics"]
        except Exception as e:
            print("Error reading config file\n" + e)
reload_config()
#Logging
logger = logging.getLogger()
loghandler = logging.handlers.WatchedFileHandler(config["logging"]["file"])
formatter = logging.Formatter(
    '%(asctime)s SANDI-Input [%(process)d]: %(message)s',
    '%b %d %H:%M:%S')
loghandler.setFormatter(formatter)
logger.addHandler(loghandler)
logger.setLevel(logging.ERROR)

#Connect to MQTT Server
mqttClient = mqtt.Client()
mqttClient.tls_set(config["mqtt"]["cacert"],config["mqtt"]["cert"],config["mqtt"]["key"])
mqttClient.connect(config["mqtt"]["host"],config["mqtt"]["port"])
logging.info("Connected to MQTT")


#Deny random defaults
@app.route('/')
def default():
    abort(404)

#Accept incoming REST messages
@app.route('/input/<string:topic>', methods=["POST"])
def publish(topic):
    #Read data input
    data = request.data
    if len(data) == 0:
        abort(400)
    if request.content_type != "application/json":
        abort(400)
    #Get client identifier
    client = request.args.get('client')
    if topic in topics:
        if client in topics[topic]:
            mqttClient.publish(topic,data)
            return '',204
        else:
            logging.error("Access denied ["+topic+"] "+request.remote_addr)
            abort(403)
    else:
        abort(404)

#Reload config
@app.route('/admin/reload')
def reload():
    client = request.args.get('client')
    if client == config["adminkey"]:
       reload_config()
       logging.info("Reloaded config")
       return '',204
    else:
        logging.error("Access denied [admin/reload] " + request.remote_addr)
        abort(403)


if __name__ == '__main__':
    app.run(host='10.10.0.1')
