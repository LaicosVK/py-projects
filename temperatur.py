import Adafruit_DHT
import time
import RPi.GPIO as GPIO
GPIO.cleanup()
        
# Set the type of sensor
sensor = Adafruit_DHT.DHT11
        
# Set the GPIO pins for each sensor
sensors = [{'name': 'eins', 'pin': 6, 'temp_min': 20.0, 'temp_max': 25, 'hum_min': 60.0, 'hum_max': 80.0}, {'name': 'zwei', 'pin': 13, 'temp_min': 20.0, 'temp_max': 25, 'hum_min': 60.0, 'hum_max': 80.0}, {'name': 'drei', 'pin': 19, 'temp_min': 20.0, 'temp_max': 25, 'hum_min': 60.0, 'hum_max': 80.0}, {'name': 'vier', 'pin': 16, 'temp_min': 20.0, 'temp_max': 25, 'hum_min': 60.0, 'hum_max': 80.0}, {'name': 'fünf', 'pin': 5, 'temp_min': 20.0, 'temp_max': 25, 'hum_min': 60.0, 'hum_max': 80.0}]
led_green = 23
led_red = 24
status_number = -5
blink_times = 5
show_debug_print = False

def main():
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
        
        def on(pin):
            debug_print(f"Turn on {pin}")
            GPIO.output(pin, True)
        def off(pin):
            debug_print(f"Turn off {pin}")
            GPIO.output(pin, False)
        
        
        def status():
            global status_number
            global blink_times
            debug_print(f"Status: {status_number}")
            
            if status_number < -10:
                status_number = -10
            if status_number > 10:
                status_number = 10
                
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
                    printt("{}: Temperatur: {:.0f}°C, Feuchtigkeit: {:.0f}%".format(part["name"], temperature, humidity))
                    if part["temp_min"] < temperature < part["temp_max"] and part["hum_min"] < humidity < part["hum_max"]:
                        status_number += 1
                    else:
                        printt("{}: Failed to pass test! Temperatur: {:.0f}°C, Feuchtigkeit: {:.0f}%".format(part["name"], temperature, humidity))
                        status_number -= 7
                else:
                    printt("Failed to get reading from sensor on pin {}".format(part["pin"]))
                    status_number -= 6
            status()
            time.sleep(10)

    except KeyboardInterrupt:
        printt('Gute nacht!')
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
