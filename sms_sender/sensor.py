import machine
from time import sleep
import logging

class Sensor():
    AirValue = 44600
    WaterValue = 17800
    def __init__(self):
        self.temperature, self.moisture = self.get_median_readings()
        
    def read_moisture(self):
        analog_value = machine.ADC(26)
        reading = analog_value.read_u16()
        percent = round(((Sensor.AirValue - reading)/(Sensor.AirValue - Sensor.WaterValue))*100,2)
        return percent

    def get_median(self, list):
        list.sort()
        mid = len(list) // 2
        res = (list[mid] + list[~mid]) / 2
        return res
        
    def read_temp(self):
        sensor_temp = machine.ADC(4)
        conversion_factor = 3.3 / (65535)
        reading = sensor_temp.read_u16() * conversion_factor
        temperature_celsius = 27 - (reading - 0.706)/0.001721
        temperature_fahrenheit = (temperature_celsius * 9 / 5 + 32) - 14
        return temperature_fahrenheit

    def get_median_readings(self):
        temps = []
        moists = []
        while len(temps) < 5:
            temp = self.read_temp()
            moist = self.read_moisture()
            temps.append(temp)
            moists.append(moist)
            position = len(temps)
            print(f"Getting {position} of 5 readings")
            sleep(.1)
        median_temp = self.get_median(temps)
        median_moisture = self.get_median(moists)
        print(f"Temperature is {median_temp} degrees F \n Moisture is {median_moisture} % ")
        logging.info(f"Temperature read: {median_temp}, Moisture read: {median_moisture} % ")
        return median_temp,median_moisture
