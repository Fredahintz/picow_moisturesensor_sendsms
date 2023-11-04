#Native libs
from machine import Pin, I2C
import network
import time
from time import sleep
import utime
import json
import logging
from ntptime import settime

#Third Party

#Internal Libs
import constants
from send_sms import send_sms, choose_message
from connect_to_network import connect_to_internet
from sensor import Sensor
logging.basicConfig(level=logging.INFO,
                    filename = "log.txt",
                    filemode="a")

led = Pin("LED", Pin.OUT)
led.toggle()

connect_to_internet(constants.SSID, constants.WIFI_PASSWORD)

while True:
    try:
        settime()
    except OSError:
        logging.error("Failed to set time")
    sensornow = Sensor()
    current_time = time.gmtime()
    formatted_time = "{:02d}/{:02d}/{} {:02d}:{:02d}".format(current_time[2], current_time[1], current_time[0], current_time[3], current_time[4])
    logging.info(f"Time is {formatted_time}")
    logging.info(f"Current Reading: Temp: {sensornow.temperature}, Moisture: {sensornow.moisture}")
    text_message = choose_message(sensornow.moisture)
    try: send_sms(
             recipient = constants.recipient_num,
             sender = constants.sender_num,
             message = text_message,
             auth_token = constants.twilio_auth,
             account_sid = constants.twilio_sid
             )
    except:
        logging.error('Failed to send SMS')
    logging.info(f'Sent SMS to {constants.recipient_num}') 
    utime.sleep(3585)

