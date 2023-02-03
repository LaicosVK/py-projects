import Adafruit_DHT
import time
from dotenv import load_dotenv
import os
import ast
import RPi.GPIO as GPIO
GPIO.cleanup()

# Variables
load_dotenv()
time_check = int(os.getenv('time_check'))
sensors = ast.literal_eval(os.getenv('sensors'))
led_green = int(os.getenv('led_green'))
led_red = int(os.getenv('led_red'))
status_number = int(os.getenv('status_number'))
blink_times = int(os.getenv('blink_times'))
status_min = int(os.getenv('status_min'))
status_max = int(os.getenv('status_max'))
show_debug_print = os.getenv('show_debug_print')
if show_debug_print == "False":
    show_debug_print = False
else:
    show_debug_print = True

sensor = Adafruit_DHT.DHT11

def main():
    global time_check
    global status_number
    try:
        # GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_green, GPIO.OUT)
        GPIO.setup(led_red, GPIO.OUT)
        
        def debug_print(text):
            global show_debug_print
            if show_debug_print:
                try:
                    print(str(text))
                except:
                    pass
                    
        def printt(text):
            try:
                print(str(text))
            except:
                pass
            
        def log(text):
            printt(text)
            f = open("log.txt", "a+")
            f.write(f"\n{time.ctime(time.time())} \t {text}")
            f.close()
        
        def on(pin):
            debug_print(f"Turn on {pin}")
            GPIO.output(pin, True)
        def off(pin):
            debug_print(f"Turn off {pin}")
            GPIO.output(pin, False)
        
        
        def status():
            global status_number
            global blink_times
            global status_min
            global status_max
            debug_print(f"Status: {status_number}")
            
            if status_number < status_min:
                status_number = status_min
            if status_number > status_max:
                status_number = status_max
                
            if status_number > 0:
                on(led_green)
                off(led_red)
        
            if status_number <= 0:
                off(led_green)
                for i in range(blink_times):
                    off(led_red)
                    time.sleep(0.2)
                    on(led_red)
                    time.sleep(0.2)
        
        
        on(led_green)
        on(led_red)
        while True:
            for part in sensors:
                humidity, temperature = Adafruit_DHT.read_retry(sensor, part["pin"])
        
                if humidity is not None and temperature is not None:
                    if part["temp_min"] <= temperature <= part["temp_max"] and part["hum_min"] <= humidity <= part["hum_max"]:
                        printt("{} Success: Temperatur: {:.0f}°C, Feuchtigkeit: {:.0f}%".format(part["name"], temperature, humidity))
                        status_number += 1
                    else:
                        log("{} Failed: Temperatur: {:.0f}°C ({}-{}), Feuchtigkeit: {:.0f}% ({}-{})".format(part['name'], temperature, part['temp_min'], part['temp_max'], humidity, part['hum_min'], part['hum_max']))
                        status_number -= 7
                else:
                    log("Failed to get reading from sensor on pin {}".format(part["pin"]))
                    status_number -= 6
            status()
            time.sleep(time_check)

    except KeyboardInterrupt:
        printt('Gute nacht!')
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        
