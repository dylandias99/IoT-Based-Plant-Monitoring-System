from flask import Flask, redirect, url_for, render_template, request
import socket
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def start():
    s = socket.socket()
    port = 9090
    s.connect(('192.168.1.147', port))
    output = input("Send a command to the client: ")
    if output == "CONNECT":
        user = "CONNECT"
        s.sendall(user.encode('utf-8'))
        light = s.recv(1024).decode('utf-8')
        temper = s.recv(1024).decode('utf-8')
        hum = s.recv(1024).decode('utf-8')
        moist = s.recv(1024).decode('utf-8')
        exit = "EXIT"
        s.sendall(exit.encode('utf-8'))
        if float(moist) < 110:
            clientId = "Omega_ADE6"
            endpoint = "abiregix44vmb-ats.iot.us-east-1.amazonaws.com"
            rootCAFilePath = "/Users/dylandias/Desktop/secondary/certs/AmazonRootCA1.pem"
            privateKeyFilePath = "/Users/dylandias/Desktop/secondary/certs/4fbc90f9de-private.pem.key"
            certFilePath = "/Users/dylandias/Desktop/secondary/certs/4fbc90f9de-certificate.pem.crt"

            print("Connecting to: " + endpoint + " ClientID: " + clientId)
            myMQTTClient = AWSIoTMQTTClient(clientId)
            print("Connected!")
            print("Subscribing to topic: Omega_ADE6/+/details")
            print("Subscribed with QoS: 1")
            myMQTTClient.configureEndpoint(endpoint, 8883)
            myMQTTClient.configureCredentials(rootCAFilePath, privateKeyFilePath, certFilePath)
            myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
            myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
            myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
            myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

            QoS = 1

            def customOnMessage(client, userdata, message):
                print(str(message.topic) + ": " + str(message.payload))

            connect_ACK = myMQTTClient.connect()
            topic = "Omega_ADE6/message"
            myMQTTClient.subscribe(topic, 1, customOnMessage)
            num = 1
            while True:
                payload = str('{"User": "Omega_ADE6",\n "Message": "The moisture value is below 50%"}')

                myMQTTClient.publish(topic, payload, 1)
                num += 1
                if (num == 2):
                    break
                time.sleep(1)

            myMQTTClient.unsubscribe(topic)
            myMQTTClient.disconnect()
            print("Test Message Sent")
        return render_template("result.html", light=light, temper=temper, hum=hum, moist=moist)
    else:
        print("Command not found")
    return "DONE"

if __name__ == "__main__":
    app.run(debug=True)
