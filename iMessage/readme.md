# iMessage adapter for SANDI
Sends notifications from MQTT queues via iMessage
## Setup
* Copy all files to a folder (like /Library/SANDI/iMessage)
* Edit plist to fit your folder and your user
* Have the specified user logged in and have the Messages app opened (can be in background)
* Edit the config file
## Config
    recipient: Recipient addresse (either iMessage mail or mobile)
    mqtt:
      host: MQTT Server IP/hostname
      port: MQTT Server port
      cacert: Path to MQTT CA certificate
      cert:  Path to MQTT client cert
      key:  Path to MQTT client key
    topics: List of topic to subscribe to. All messages received on these topics will be sent.
