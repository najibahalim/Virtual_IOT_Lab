
# use the following commands first 
#  pip install pep8
#  pip install AWSIoTPythonSDK
#  pip install requests
#  pip install json
#  pip install datetime


#import requests package for getting API responses
import requests
# import time module for getting the required pause in *seconds*
import time
# import datetime module for getting the timestamp
from datetime import datetime
# install AWS Python SDK, you can install it as pip install boto3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
# import json module for creating and handeling json
import json
from boto3 import resource
from boto3.dynamodb.conditions import Key
import time
import uuid
from datetime import datetime
from decimal import Decimal

from dynamodb_json import json_util as jsonu
import random
import string

conn = resource('dynamodb')
table = conn.Table('Tempereature')

# API calls for different cities temperature from openweathermap api
url1 = 'http://api.openweathermap.org/data/2.5/weather?appid=f6182a9874fa6e1a215f5a7489f8b3eb&q=Mumbai'
url2 = 'http://api.openweathermap.org/data/2.5/weather?appid=f6182a9874fa6e1a215f5a7489f8b3eb&q=Lonavala'
url3 = 'http://api.openweathermap.org/data/2.5/weather?appid=f6182a9874fa6e1a215f5a7489f8b3eb&q=Pune'

# intializing MQTT client which will send MQTT request to the AWS IOT service 
# the required public key, private key and the root-ca certificate will be provided by AWS in the process 
# creating AWS Device
# for this AWS IoT device we have provided access to all resouces in policy
myMQTTClient = AWSIoTMQTTClient("Temp_sensor")
myMQTTClient.configureEndpoint("a3afa41mc06g6e.iot.us-west-2.amazonaws.com",8883)
myMQTTClient.configureCredentials("root-CA.crt","Temp_sensor.private.key","Temp_sensor.cert.pem")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("Temp_sensor/info", "connected", 0)

#loop for sending the readings to the AWS IoT and storing it into DynamoDB
count = 0
key = list()
while count < 2:
    data = {}
    json1 = requests.get(url1).json()
    json2 = requests.get(url2).json()
    json3 = requests.get(url3).json()
    data['key']=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    key.append(data['key'])
    data['Mumbai']="{0:.2f}".format(float(json1['main']['temp'])-273.15)
    data['Lonavala'] = "{0:.2f}".format(float(json2['main']['temp'])-273.15)
    data['Pune'] ="{0:.2f}".format(float(json3['main']['temp'])-273.15)
    data['timestamp'] = str(datetime.now())
    data['count']=count
    payload = json.dumps(data)
    print(payload)
   
    myMQTTClient.publish("Temp_sensor/data",payload,0)
    time.sleep(2)
    count = count+1
count = 0
out = {}

for itr in key:
    print(itr)
    print(count)
    info={}
    info['key']=itr
    info['count']=count
    item = table.get_item(
        Key={
            'key':itr,
            'count':count
        }
    )
    print(item)
    out[count] = jsonu.loads(item['Item']['payload'])

    count = count +1
file = open("output.json","a")
json.dump(out,file,indent=4,sort_keys=True)    
file.close()


