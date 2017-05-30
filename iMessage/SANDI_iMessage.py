from paho.mqtt import client as mqtt
from yaml import load
import os


template = """ osascript -e '
        tell application "Messages"
        set targetService to 1st service whose service type=iMessage
        set targetBuddy to buddy "___NAME___" of targetService
        send "___MESSAGE___" to targetBuddy
        end tell'
    """
recipient=""
topics = dict()
mqttClient = mqtt.Client()
def main():

    base = os.path.dirname(os.path.realpath(__file__))
    with open(base + "/config.yml", 'r') as file:
        try:
            config = (load(file))
            global topics
            topics = config["topics"]
            global recipient
            recipient = config["recipient"]
        except Exception as e:
            print("Error reading config file\n" + e.message)

    mqttClient.on_message = on_message
    mqttClient.on_connect = on_connect
    mqttClient.tls_set(config["mqtt"]["cacert"], config["mqtt"]["cert"], config["mqtt"]["key"])
    mqttClient.connect(config["mqtt"]["host"], config["mqtt"]["port"])
    mqttClient.loop_forever()

def on_message(client,userdata,msg):
    message = str(msg.payload)
    sendMessage(message)

def on_connect(client, userdata, flags, rc):
    for topic in topics:
        print(topic)
        mqttClient.subscribe(topic)

def sendMessage(body):
    #Todo: remove all " and '
    cmd = template.replace("___MESSAGE___", body)
    cmd = cmd.replace("___NAME___",recipient)
    os.system(cmd)

if __name__ == "__main__":
    main()