from network import WLAN
from machine import Pin, PWM, Timer
import umqtt.robust as umqtt
import time
from machine import ADC

import lab10_upb2 as lab10 


""" Connection stuff """
wifi = WLAN(WLAN.IF_STA)
wifi.active(True) 

# Variable Connection info
ssid = "Dyln"
password = "eesy7794"
port_number = 80

temp_sensor = ADC(4)


# Pi Connection Area
BROKER_IP = '10.111.224.91'
PORT = 8080
TOPIC = 'temp/pico'
PUB_IDENT = 3
    
# Function to connect to wifi
def connect(wifi_obj, ssid, password, timeout=10):
    wifi_obj.connect(ssid, password) 

    while timeout > 0: 
        if wifi_obj.status() != 3: 
            time.sleep(1) 
            timeout -= 1 
        else: 
            return True 
    return False

# Connection to wifi
if not connect(wifi, ssid, password):
    print("Wifi Not Connected")
else:
    print("Connected")
    
    
""" MQTT Area"""
mqtt = umqtt.MQTTClient(
    client_id = b'publish',
    server = BROKER_IP.encode(),
    port = PORT,
    keepalive = 7000
    )
mqtt.connect()

# Read the temperature from sensor
def read_temp(t):
    """Reads the temperature every time the timer ends"""
    global temp_sensor, mqtt
    
    # Conversion formula
    value = temp_sensor.read_u16()
    voltage = value * (3.3 / 2 ** 16)
    temperature = 27 - (voltage - 0.706) / 0.001721
    
    proto_message = lab10.MeowMessage()
    proto_message.client_id = PUB_IDENT
    proto_message.temperature = temperature
    proto_message.time = time.time()
    print(temperature)
    mqtt.publish(TOPIC, proto_message.serialize())
    

# Wait timer for temperature read
timer = machine.Timer()
timer.init(freq=0.5, mode=machine.Timer.PERIODIC, callback=read_temp)


#message = array[i] 

#newmessage = parse(message)
